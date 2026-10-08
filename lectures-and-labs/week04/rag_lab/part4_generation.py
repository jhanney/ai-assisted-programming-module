"""
Part 4: Generation -- RAG Lab

In this part, you will:
1. Connect to a hosted model through an OpenAI-compatible API
2. Build a grounded prompt from retrieved chunks
3. Complete the pipeline: retrieve, augment, generate
4. Return the answer together with the documents it came from

Run it as:   python part4_generation.py

Estimated time: 30 minutes
"""

import os

import chromadb
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer

COLLECTION = "cs_knowledge"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# The generation half talks to a hosted model through the OpenAI-compatible
# API that most providers now offer, so the provider is a setting, not code.
# .env supplies three values (see .env.example): the key, the base URL and
# the model name. The defaults point at the Gemini API's free tier.
DEFAULT_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
DEFAULT_MODEL = "gemini-3.5-flash-lite"

# The grounding instruction. The permission to say "I don't know" is
# load-bearing (see the README): without it the most plausible completion
# is a confident answer from training data, which is the failure grounding
# exists to prevent.
GROUNDING_RULES = (
    "Answer the question using ONLY the context below. "
    "If the context does not contain the answer, reply exactly: "
    "I don't know - the provided context does not cover this. Do not add "
    "anything to that refusal. For an answer supported by the context, "
    "finish with the document you used, in square brackets, like "
    "[source: introduction_to_programming.txt]."
)


def llm_settings():
    """Return (api_key, base_url, model) from .env, with the defaults above."""
    load_dotenv()
    return (os.getenv("LLM_API_KEY"),
            os.getenv("LLM_BASE_URL", DEFAULT_BASE_URL),
            os.getenv("LLM_MODEL", DEFAULT_MODEL))


def initialize_llm():
    """
    Initialize the client for the hosted model.

    Returns:
        OpenAI client object, or None when no key is set
    """
    api_key, base_url, _ = llm_settings()
    if not api_key:
        return None
    return OpenAI(api_key=api_key, base_url=base_url)


def build_rag_prompt(query, context_chunks):
    """
    Build a grounded prompt from the retrieved chunks and the question.

    Args:
        query: The question
        context_chunks: List of (chunk_text, source) pairs, best first

    Returns:
        The prompt string
    """
    context = "\n\n".join(
        f"[source: {source}]\n{text}"
        for text, source in context_chunks
    )
    return (
        f"{GROUNDING_RULES}\n\n"
        f"CONTEXT:\n{context}\n\n"
        f"QUESTION: {query}\n\n"
        "ANSWER:"
    )


def call_llm(client, prompt, max_tokens=500):
    """
    Call the hosted model with the given prompt.

    Args:
        client: OpenAI client (from initialize_llm)
        prompt: The formatted prompt
        max_tokens: Maximum tokens in the response

    Returns:
        Generated response text
    """
    _, _, model = llm_settings()
    response = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def rag_query(question, collection, embedding_model, llm_client, top_k=3):
    """
    Complete RAG pipeline: retrieve, augment, generate.

    Args:
        question: The question
        collection: ChromaDB collection
        embedding_model: SentenceTransformer model -- the same one as part 2
        llm_client: OpenAI client, or None to retrieve without generating
        top_k: Number of chunks to retrieve

    Returns:
        dict with 'answer' (str or None), 'sources' (list of filenames,
        best first, no repeats) and 'context_used' (list of chunk texts)
    """
    query_embedding = embedding_model.encode(question)
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k,
    )
    texts = results["documents"][0]
    sources = [metadata["source"] for metadata in results["metadatas"][0]]
    context_chunks = list(zip(texts, sources))
    prompt = build_rag_prompt(question, context_chunks)
    answer = call_llm(llm_client, prompt) if llm_client else None

    return {
        "answer": answer,
        "sources": list(dict.fromkeys(sources)),
        "context_used": texts,
    }


def test_rag_system():
    """Ask the questions DIY 5 names, and show the answer with its source."""
    print("=" * 70)
    print("Part 4: Generation")
    print("=" * 70)
    print()

    embedding_model = SentenceTransformer(EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path="./chroma_db")
    try:
        collection = client.get_collection(name=COLLECTION)
        print(f"Found {collection.count()} chunks in the index")
    except Exception:
        print("Index not found. Run part2_embeddings.py first.")
        return

    llm_client = initialize_llm()
    if llm_client is None:
        print("No LLM_API_KEY in .env - retrieval will run, generation is skipped.")
        print("Copy .env.example to .env and add a free key (the README says where).")
    print()

    questions = [
        "What is a variable?",
        "How do linked lists work?",
        "How do I bake sourdough?",   # not in the corpus: the model must decline
    ]

    for question in questions:
        try:
            result = rag_query(question, collection, embedding_model, llm_client, top_k=3)
        except Exception as e:
            print(f"Error processing question: {e}")
            print("Check your implementation and try again")
            print()
            continue
        if not result:
            print(f"Q: {question}")
            print("   rag_query() returned nothing - check your implementation")
            print()
            continue
        print(f"Q: {question}")
        print(f"A: {result.get('answer') or '(no key set - retrieval only)'}")
        sources = result.get("sources") or []
        print(f"   retrieved from: {', '.join(sources) if sources else 'nothing'}")
        print()

    print("=" * 70)
    print("Part 4 complete. Next: python part5_experiments.py")
    print("=" * 70)


def interactive_mode():
    """Ask your own questions."""
    print("\n" + "=" * 70)
    print("Interactive mode - type a question, or 'quit'")
    print("=" * 70)

    embedding_model = SentenceTransformer(EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(name=COLLECTION)
    llm_client = initialize_llm()

    while True:
        question = input("\nQ: ").strip()
        if question.lower() in ("quit", "exit", "q"):
            break
        if not question:
            continue
        try:
            result = rag_query(question, collection, embedding_model, llm_client)
            if result:
                print(f"A: {result['answer']}")
                print(f"   retrieved from: {', '.join(result.get('sources') or [])}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    test_rag_system()

    # Uncomment for interactive mode:
    # interactive_mode()
