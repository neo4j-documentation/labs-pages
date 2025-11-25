from mcp.server import MCPServer, MCPTool
from neo4j import GraphDatabase
import os

# Configurazione Neo4j
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "test")

# Tool MCP per eseguire query Neo4j
class Neo4jQueryTool(MCPTool):
    name = "neo4j_query"

    def run(self, query: str):
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        try:
            with driver.session() as session:
                result = session.run(query)
                # Convertiamo i record in lista di dict
                return [record.data() for record in result]
        finally:
            driver.close()

if __name__ == "__main__":
    # Avvio MCP server HTTP
    server = MCPServer(host="0.0.0.0", port=8000, tools=[Neo4jQueryTool()])
    print("MCP Neo4j server running at http://localhost:8000/mcp")
    server.start()
