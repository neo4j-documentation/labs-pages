from mcp.server import FastMCP
from neo4j import GraphDatabase
import os

# Configurazione Neo4j
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "apoc12345")

# Crea il server MCP
mcp = FastMCP("Neo4j MCP Server")

@mcp.tool(description="Esegui una query Neo4j e ritorna il risultato")
def neo4j_query(query: str):
    """
    Esegue la query Neo4j passata come stringa e ritorna il risultato come lista di dizionari.
    """
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    try:
        with driver.session() as session:
            print(f"Eseguendo query: {query}")  # ← qui vedrai il log
            result = session.run(query)
            return [record.data() for record in result]
    finally:
        driver.close()

if __name__ == "__main__":
    print("MCP Neo4j server in esecuzione su http://localhost:8000/mcp")
    mcp.run(transport="streamable-http")
