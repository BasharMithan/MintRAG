# MintRAG: A Sample Knowledge Base

MintRAG turns a collection of readable source documents into material that can be searched and retrieved in useful pieces. This sample introduces the project’s basic ingestion ideas: load a document, divide it into overlapping chunks, and retain enough context for each chunk to make sense on its own. It is intentionally written as a small knowledge-base article rather than as a list of test strings.

## Why retrieval uses chunks

A long document may contain several topics, examples, and definitions. Sending the entire document to a search or language model for every question is often inefficient, and a single large result can obscure the passage that actually answers the question. Chunking creates smaller units that can be indexed and selected independently, while preserving their relationship to the original source.

Useful chunks are not merely short. They should carry a coherent thought: a definition with its explanation, a procedure with its important conditions, or an example with the lesson it demonstrates. Headings and paragraph breaks help readers navigate the source and give retrieval systems meaningful structure to work with. MintRAG’s character-based splitter uses a predictable size limit, so content authors should also write clear transitions and avoid relying on distant context.

## From source file to document

The ingestion process begins by loading a source file as text. A document represents that text together with identifying information, including its source and a stable identity derived from the loaded content. Keeping source information alongside the text makes it possible to connect a retrieved passage back to where it came from.

Markdown is a convenient format for this sample because it is easy to review, edit, and version. The heading hierarchy describes the subject, while ordinary paragraphs provide the actual explanations that a reader may want to retrieve. Other formats can be supported by loaders that convert their contents into the same document representation. Regardless of format, preserving readable text and reliable source details makes downstream retrieval more useful.

## How character chunking works

The default `CharacterChunker` configuration limits each chunk to 1,000 characters and overlaps neighboring chunks by 150 characters. After emitting one chunk, the splitter advances by the chunk size minus the overlap. This means the end of one passage is repeated at the beginning of the next, allowing a sentence or connected idea near a boundary to retain some of its context.

For example, a paragraph may begin near the end of one chunk and continue into the next. The overlap gives both pieces a shared stretch of text, reducing the chance that a relevant detail becomes detached from the statement that explains it. Overlap does not replace thoughtful document structure, however: a heading should still introduce the section it describes, and paragraphs should still focus on a manageable subject.

Chunk size and overlap are configurable because sources differ. A compact FAQ may benefit from smaller passages, while technical explanations can require more surrounding context. The overlap must remain smaller than the chunk size so that each step moves forward. When adjusting these values, inspect actual chunks and consider whether they preserve useful context without repeating too much material.

## Writing for reliable retrieval

Prefer descriptive headings over generic labels. A heading such as “How character chunking works” tells readers what follows, while a label such as “Details” does not. Begin paragraphs with their main point, define specialized terms before relying on them, and spell out abbreviations when they first appear. These habits help both people and retrieval systems identify the subject of an isolated passage.

Keep related steps together and make important conditions explicit. If a procedure depends on a setting, state the setting close to the procedure. If a recommendation has an exception, include the exception in the same section. Avoid using phrases such as “as noted above” when the explanation may be separated into another chunk; repeat the necessary detail briefly instead of making a passage depend on unavailable context.

Lists and examples can make complex material easier to scan, but they should have a clear introduction and interpretation. A list of terms without definitions may be difficult to retrieve accurately, and an example without an explanation may be ambiguous. This sample uses complete paragraphs so that its sections remain meaningful even when a chunk begins or ends partway through the source.

## Reviewing generated chunks

After loading a document, inspect the resulting chunks before indexing them. Check that the text is nonempty, that chunk boundaries move through the document in order, and that neighboring passages share the configured amount of context. Look for headings separated from their explanations, sentences split in confusing places, or repeated text that dominates the useful content.

Chunk identifiers can be generated from document identity, configuration, and character boundaries. This makes a chunk addressable within a particular split of a document, while the source metadata preserves its provenance. If the document or chunking settings change, the resulting boundaries may also change; retrieval should therefore use the current chunks produced from the current source.

## A practical retrieval workflow

Once chunks have been created, an application can represent them as vectors, store those vectors with their source metadata, and compare a question with the indexed content. The closest passages become candidates for a response. Retrieval quality depends on the full chain: accurate source text, sensible chunk boundaries, useful representations, and a search strategy suited to the question.

A good workflow evaluates results with realistic questions rather than relying only on successful file loading. Ask questions whose answers are in different sections, then confirm that the selected passages contain enough information to answer them. If results omit an important condition or include unrelated material, review the source wording and chunk boundaries before changing later stages of the system.

## Summary

MintRAG’s sample demonstrates how a structured Markdown article can provide several clear retrieval passages. Descriptive sections establish topics, focused paragraphs explain them, and modest overlap helps preserve continuity across character-based boundaries. These principles offer a useful starting point for building and evaluating document-ingestion workflows.
