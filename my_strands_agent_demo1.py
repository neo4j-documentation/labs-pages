# my_strands_agent_demo.py
from strands import Agent
from strands.models.mistral import MistralModel
from strands.tools.mcp.mcp_client import MCPClient
from mcp.client.streamable_http import streamablehttp_client

# Transport MCP via HTTP
def create_transport():
    return streamablehttp_client("http://localhost:8000/mcp/")

mcp_client = MCPClient(create_transport)

if __name__ == "__main__":
    with mcp_client:
        # Lista dei tool MCP
        tools = mcp_client.list_tools_sync()
        print("TOOLS DISPONIBILI:", [t.mcp_tool.name for t in tools])

        # Trova il tool Neo4j
        neo4j_tool = next(t for t in tools if t.mcp_tool.name == "neo4j_tool")

        # Agent MistralModel
        agent = Agent(
            model=MistralModel(
                api_key="LA_TUA_MISTRAL_API_KEY",
                model_id="mistral-large-latest",
                max_tokens=300,
                temperature=0.7,
            ),
            tools=tools
        )

        # Esempio query Neo4j tramite tool MCP
        query = "MATCH (p:Person) RETURN count(p) AS c"
        result = neo4j_tool.run({"query": query})
        print("RISULTATO NEO4J:", result)
