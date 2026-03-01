# Multi-Agent PDF Chat

This project is a small multi-agent system which answers questions about PDFs given in the knowledge base. For the purpose of this project, the paper 'Attention Is All You Need' is used as a sample PDF.

## How it works

- PDF Agent: answers using the PDF
- Web Agent: searches online if the paper doesn't contain an answer for the user's query
- Coordinator: combines the results to form the final response

The coordinator agent routes each query to the PDF agent or web agent, preferring to answer from the PDF whenever possible, citing its sources in the final answer.

## Tech stack

- Agno
- LanceDB
- Groq (Llama-3.3-70B and Qwen3-32B)
- DuckDuckGo search tool
- Python + uv

## Running the project

Get your API keys from:  
https://console.groq.com/keys  
https://aistudio.google.com/app/api-keys

Create a `.env` file with your API keys:

GROQ_API_KEY=your_key  
GOOGLE_API_KEY=your_key  

Install dependencies:  
`uv sync`

Run:  
`uv run main.py`

## Sample questions

- Summarize the paper.
- Explain the model architecture.
- Why is positional encoding required?

## Notes

After the first run, comment out the `knowledge_base.insert()` part to avoid inserting the same document again.