1. PROBLEM STATEMENT (Domain-Specific, 500–800 words)
Multimodal Intelligent Assistant for Automotive Owner Manuals

Modern vehicles like the Tata Safari come with highly detailed owner manuals (as seen in your PDF), containing hundreds of pages of text instructions, structured tables, warning labels, and visual diagrams. While these manuals are comprehensive, they are not user-friendly for real-time problem-solving.

For example, a user may ask:

“What should I do if my car gets flooded?”
“What does the ABS warning light mean?”
“How do I use child lock?”
“Explain this dashboard symbol (image)”

Traditional keyword-based search fails in such scenarios because:

Contextual understanding is missing — searching “water” won’t retrieve “Driving Through Water” advice properly.
Multimodal content is ignored — images (dashboard icons, diagrams) are not searchable.
Tables are hard to query — e.g., CRS seating tables are structured but not easily retrievable.
Natural language queries don’t map to document structure.

From your PDF:

Safety instructions (text-heavy)
CRS tables (structured data)
Dashboard icons (visual)
Warning labels (semantic importance)

This makes it a perfect multimodal problem.

❗ Why Multimodal Understanding is Required

The manual contains:

Text → driving instructions, warnings
Tables → child restraint system recommendations
Images/diagrams → dashboard indicators, airbag placement

A user might upload:

A photo of a warning light
A screenshot of a table
A query referencing a diagram

Thus, system must:

Understand text
Interpret tables
Analyze images
🚀 Why RAG is the Best Solution

A Retrieval-Augmented Generation (RAG) system:

Retrieves relevant chunks from the manual
Uses an LLM to generate contextual answers

Benefits:

No hallucination → grounded in manual
Scalable → works for any vehicle manual
Explainable → shows source context
🎯 Example Queries
Text Query

“How to drive in heavy rain?”

→ Retrieves “Driving on Wet Roads”

Table Query

“Where should a 3-year-old child sit?”

→ Retrieves CRS table

Image Query

Upload dashboard warning light

→ Vision model explains symbol

✅ Expected Outcomes
Accurate answers grounded in manual
Multimodal query support
Real-time API-based system
Scalable for multiple vehicles

2. SYSTEM ARCHITECTURE
🔷 Components
1. Ingestion Pipeline
Extract text, tables, images from PDF
2. Processing Layer
Chunking
Metadata tagging
3. Embedding Layer
Convert content → vectors
4. Vector Store
Store embeddings (FAISS/Chroma)
5. Retrieval Pipeline
Semantic search
6. RAG Generation
LLM + retrieved context
7. FastAPI Layer
REST APIs

Mermaid Diagram

<img width="1744" height="1912" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/56c5f334-10ba-4ac6-a9a5-9ef78e57ea95" />

