from strands import Agent
from strands.models.mistral import MistralModel
from strands.tools.mcp import MCPClient
import os

# Import del client HTTP MCP (streamable)
try:
    from mcp.client.streamable_http import streamablehttp_client
except ImportError:
    # fallback se la versione mcp è differente
    from mcp.client.http import http_client as streamablehttp_client

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

def create_transport():
    # Qui indichi l'endpoint HTTP del tuo server MCP
    # Assicurati che il percorso corrisponda a quello usato da FastMCP (es. /mcp)
    return streamablehttp_client("http://localhost:8000/mcp")

mcp_client = MCPClient(create_transport)

if __name__ == "__main__":
    with mcp_client:
        tools = mcp_client.list_tools_sync()
        print("TOOLS disponibili dal server MCP:", [t.name for t in tools])

        # Crea l’agente Strands con Mistral
        model = MistralModel(
            api_key=MISTRAL_API_KEY,  # metti la tua chiave Mistral
            model_id="mistral-small-latest",
            max_tokens=200,
            temperature=0.7,
        )

        agent = Agent(model=model, tools=tools)

        # Prompt: chiedi di eseguire una query tramite il tool Neo4j
        prompt = "Esegui questa query Neo4j e dimmi il risultato: `MATCH (n) RETURN n LIMIT 5`"
        result = agent(prompt)

        # Stampa il risultato restituito dall'agente
        # a seconda della versione di Strands, può essere result.output o str(result)
        try:
            print("RISULTATO:", result.output)
        except AttributeError:
            print("RISULTATO:", result)
