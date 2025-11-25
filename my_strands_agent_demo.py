from strands import Agent
from strands.models.mistral import MistralModel
from strands.tools.mcp.mcp_client import MCPClient
from mcp.client.streamable_http import streamablehttp_client
from mcp_neo4j_tool import MCPNeo4jTool

# --- Configura il trasporto MCP (HTTP) ---
def create_transport():
    return streamablehttp_client("http://localhost:8000/mcp")  # MCP server endpoint

mcp_client = MCPClient(create_transport)

# --- Configura Neo4j ---
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"

neo4j_tool = MCPNeo4jTool("neo4j_tool", NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

if __name__ == "__main__":
    with mcp_client:
        # Puoi aggiungere tool custom al client MCP
        tools = mcp_client.list_tools_sync()
        tools.append(neo4j_tool)  # Aggiungi il tool Neo4j

        print("TOOLS disponibili:", [t.name for t in tools])

        # --- Crea l'agente con Mistral ---
        model = MistralModel(
            api_key="LA_TUA_MISTRAL_API_KEY",
            model_id="mistral-small-latest",
            max_tokens=200,
            temperature=0.7,
        )

        agent = Agent(model=model, tools=tools)

        # --- Prompt con query Neo4j reale ---
        prompt = {
            "tool": "neo4j_tool",
            "arguments": {"query": "MATCH (n) RETURN n LIMIT 5"}
        }

        result = agent(prompt)

        try:
            print("RISULTATO:", result.output)
        except AttributeError:
            print("RISULTATO:", result)
