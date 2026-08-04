* flow
Question
      │
      ▼
Prompt
      │
      ▼
Gemini
      │
      ▼
Summary
      │
      ▼
RunnableLambda
(add metadata)
      │
      ▼
RunnableParallel
      │
 ┌────┼───────────┐
 ▼    ▼           ▼
Quiz Keywords Examples
      │
      ▼
RunnablePassthrough
      │
      ▼
Final Report

* Output:
{
    "question": "...",
    "summary": "...",
    "metadata": {
        "words": ...,
        "reading_time": ...
    },
    "quiz": "...",
    "keywords": [...],
    "examples": "..."
}
