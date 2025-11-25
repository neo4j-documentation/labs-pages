from strands.tools.mcp.mcp_client import MCPClient
from mcp.server.streamable_http import StreamableHTTPMCPServer
from mcp_neo4j_tool import MCPNeo4jTool

# --- Configurazione Neo4j ---
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"

# --- Inizializza il tool Neo4j ---
neo4j_tool = MCPNeo4jTool("neo4j_tool", NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

# --- Crea server MCP HTTP ---
server = StreamableHTTPMCPServer(
    host="0.0.0.0",
    port=8000,
    tools=[neo4j_tool]  # esponiamo il tool Neo4j
)

if __name__ == "__main__":
    print("MCP Neo4j Server in avvio su http://localhost:8000/mcp …")
    server.run()
