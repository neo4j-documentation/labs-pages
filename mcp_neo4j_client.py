# mcp_client_example_mistral.py

from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.tools.mcp.mcp_client import MCPClient

# IMPORT MODELLO MISTRAL
from strands.models.mistral import MistralModel
import os
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

def create_streamable_http_transport():
    # L’URL deve essere quello del tuo server FastMCP
    return streamablehttp_client("http://localhost:8000/mcp/")


def main():
    # 1) Crea client MCP
    streamable_http_mcp_client = MCPClient(create_streamable_http_transport)

    with streamable_http_mcp_client:
        # 2) Lista tool MCP
        tools = streamable_http_mcp_client.list_tools_sync()
        print("TOOLS disponibili:", [getattr(t, "name", t.mcp_tool.name) for t in tools])

        # 3) Crea l'agente con Mistral
        agent = Agent(
            tools=tools,
            model=MistralModel(
                api_key=MISTRAL_API_KEY,
                model_id="mistral-small-latest",
                temperature=0.7,
                max_tokens=200,
            ),
        )

        # 4) Esegui domanda tramite agente
        response = agent("What is 125 plus 375?")
        print("Risposta agente:", response)

        # 5) Oppure invoca il tool direttamente
        result = streamable_http_mcp_client.call_tool_sync(
            tool_use_id="tool-1",
            name="neo4j_query",
            arguments={"x": 125, "y": 375},
        )
        print("Risultato calcolatore:", result["content"][0]["text"])


if __name__ == "__main__":
    main()
