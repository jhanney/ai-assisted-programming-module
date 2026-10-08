# RAG Lab - results

**Name:** _[Your name]_
**Date:** _[Date]_

Fill this in as you go. The README says what each section is for.

---

## Part 1: chunking and embeddings (DIY 1 and 2)

- Documents loaded: ___
- Chunks produced at 200 words: ___ (shortest ___ words, longest ___ words)
- Vector dimensionality: ___
- Did the query vector have the same dimensionality as the chunks? ___

_What did the overlap check show?_

---

## Part 2: retrieval (DIY 3 and 4)

**"what is a variable"** - top hit, score and source: ___

**"how can my code remember a number for later"** - top hit, score and source: ___

_Same meaning, different words: did both queries find the same chunk?_

**"how do I bake sourdough"** - what came back, and with what scores: ___

_One sentence on what a retrieval system does when nothing is relevant:_

---

## Part 3: grounding (DIY 5)

**Q:** What is a variable?
**A:** ___
**Source it cited:** ___

**Q:** How do I bake sourdough?
**A:** ___ (did it decline?)

---

## Part 4: chunk size (DIY 6)

| Chunk size | Right chunk found? | Noise | Notes |
|------------|--------------------|-------|-------|
| 50 words   | Yes for both variable queries; no sourdough answer | 150 words across the top 3 | Most focused results, but the top variable chunk starts mid-thought: "stores information." |
| 200 words  | Yes for both variable queries; no sourdough answer | 512 words for variable queries; 600 for sourdough | The definition is in the top hit; other retrieved chunks add unrelated text. |
| 800 words  | Yes for both variable queries; no sourdough answer | 1,108 words for variable queries; 1,154 for sourdough | Retrieval returns large document-sized chunks, bringing substantially more unrelated text. |

With 50-word chunks, a useful fact can lose the context that explains what it is about; with 800-word chunks, the fact is buried in much more unrelated text.

_Measured with a fixed 20-word overlap and top 3 results; word totals count the full returned chunks, including any repeated overlap._

---

## Part 5: long context versus retrieval (DIY 7)

```text
Whole corpus size: 1,970 words, approximately 2,626 tokens (words / 0.75)

Question asked: What is a variable?
  RAG answer: A variable is like a labeled box that stores information.
  Whole-corpus answer: Same answer.
Which was better? No difference.

Question asked: How do linked lists work?
  RAG answer: Nodes hold data and links; singly linked lists point forward,
  doubly linked lists point both ways.
  Whole-corpus answer: Same core explanation, plus that insertions and
  deletions can avoid shifting array elements.
Which was better? Whole corpus gave one extra relevant detail.

Question asked: What is HTML?
  RAG answer: HTML provides page structure and content using tags such as
  headings, paragraphs, links and images.
  Whole-corpus answer: HTML provides the structure and content of web pages.
Which was better? RAG gave more of the details in the retrieved context.

Overall: No consistent winner; both answered from the labelled corpus and
cited the relevant document. At what corpus size would this flip? When the
whole corpus no longer fits the model's context window or becomes too costly
or slow to send; retrieval also helps when freshness and targeted citations
matter.
```

**The question the corpus cannot answer** (sourdough):

- No context: ___
- Whole corpus: ___
- RAG: ___

_Which of the three declined, and what made the difference?_

---

## Reflection

_When would you build retrieval, and when would you just paste everything?_

_What surprised you?_
