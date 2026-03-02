import typer
from agno.team import Team
from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.vectordb.lancedb import LanceDb
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.models.groq import Groq
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.models.google import Gemini
from rich.prompt import Prompt

from dotenv import load_dotenv

load_dotenv()

knowledge_base = Knowledge(
    vector_db=LanceDb(
        table_name="pdf_documents",
        uri="tmp/lancedb",
        embedder=GeminiEmbedder(),
    ),
)

# Comment out after first run
knowledge_base.insert(
    path="data/pdfs",
    reader=PDFReader(),
)

def lancedb_agent(user: str = "User"):
    pdf_agent=Agent(
        name="PDF Agent",
        model=Gemini(id="gemini-2.5-flash"),
        knowledge=knowledge_base,
        search_knowledge=True,
        instructions="""
        Use this agent to answer questions based on the PDF documents in the knowledge base.
        Answer only from the knowledge base. If the answer is not present, say it is not found in the PDFs.
        Include the source page or section when possible.""",
        markdown=True,
    )

    web_agent=Agent(
        name="Web Agent",
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=[DuckDuckGoTools()],
        instructions="""
        Use this agent only when the PDF agent cannot answer the question.
        Always return concise factual information from the web.
        Include the source website for each piece of information.""",
        markdown=True,
    )

    agent_team=Team(
        members=[pdf_agent, web_agent],
        model=Groq(id="qwen/qwen3-32b"),
        description="""
        You are a coordinator for a team of specialist agents that answer user queries.
        Alawys use the PDF Agent first to find answers in the knowledge base.
        If the answer is missing, only then use the Web Agent.
        Base the final response only on agent outputs.
        Always specify the source for each part of the response. Also state whether it was obtained from the PDFs or the web.
        """,
        markdown=True,
    )

    while True:
        message = Prompt.ask(f"[bold] :sunglasses: {user} [/bold]")
        if message in ("exit", "bye", "quit"):
            break
        agent_team.print_response(message, session_id=f"{user}_session")

if __name__ == "__main__":
    typer.run(lancedb_agent)