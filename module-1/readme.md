## Why RAG Exists?

## The Core problem With LLMS
- Large Language Models like GPT do not store facts like database
- They work predicting next tokens based on probabilities.
- Like `User Inputs -> Tokenization -> Neural Network -> Next token Prediction`
  ```
    Example:
    Prompt: The capital of France is: 
  
    Model Predicts:
    France
    Reasoning: Because during trainings it saw this patterns many times
    ```
## Three Critical Problems

### 1. Knowledge Cutoff
- LLMs only knows what they were trained on
- So if you ask the LLM
  ```
    What happened in the 2025 US election?
    If the model trained on data up to 2023, it cannot know.
    ```

### 2. Hallucinations
- If the model doesn't know, it still tries to answer.
  ```
    Example:
    Give me the paper "Attention is All You Need 2"
    
    Possible Output:
    "Attention is All You Need 2 was published in 2021..."
  ```

### 3. Context Window
- LLM have limited memory per request
  ```
  So if you feed data that exceeds the token limit. It cannot fit
  
  Prompt:
  Here are 300 pages of documentation.
  <PASTE EVERYTHING>

  Now answer: How does the billing system work?
  ```
  - Problems:
    - Too large
    - Expensive
    - Slow
    - Still inaccurate

## The Solution is RAG
- Instead of sending everything
  ```
    User Question
          ↓
    Search relevant documents
          ↓
    Insert only relevant chunks into prompt
          ↓
    LLM generates answer
  ```
- Architecture
  ```
    User Question
          │
          ▼
    Retriever (vector DB)
          │
          ▼
    Relevant documents
          │
          ▼
    Prompt + Context
          │
          ▼
    LLM
          │
          ▼
    Answer
    ```
- This Solves

  | Problem          | Solution                    |
  | ---------------- | --------------------------- |
  | Knowledge cutoff | Use fresh data              |
  | Hallucinations   | Ground answers in documents |
  | Context limit    | Send only relevant chunks   |
