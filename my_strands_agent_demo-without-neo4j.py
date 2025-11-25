from strands import Agent
from strands.models.mistral import MistralModel
from strands.tools.mcp.mcp_client import MCPClient
import os
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# IMPORT del client HTTP fallback fornito dal pacchetto MCP
try:
    from mcp.client.streamable_http import streamablehttp_client
except ImportError:
    raise ImportError("streamablehttp_client non trovato. Controlla l'installazione del pacchetto MCP.")

# Factory per creare il trasporto MCP HTTP
def create_streamable_http_transport():
    return streamablehttp_client("http://localhost:8000/mcp/")  # URL del tuo server MCP

# --- MCPClient --- #
mcp_client = MCPClient(create_streamable_http_transport)

# --- Main --- #
if __name__ == "__main__":
    with mcp_client:
        # Recupera i tool disponibili dal server MCP
        tools = mcp_client.list_tools_sync()
        print("TOOLS disponibili:", [t.mcp_tool.name for t in tools])

        # Crea l'agente con Mistral e i tool MCP
        agent = Agent(
            model=MistralModel(
                api_key=MISTRAL_API_KEY,
                model_id="mistral-large-latest",
                max_tokens=300,
                temperature=0.7,
            ),
            tools=tools
        )

        # Esempio: query Neo4j via tool MCP
        question = "MATCH (p:Person) RETURN count(p) AS c"
        result = agent(question)
        try:
            print("RISULTATO:", result.output)
        except AttributeError:
            # fallback se l'oggetto result non ha output
            print("RISULTATO:", result)
