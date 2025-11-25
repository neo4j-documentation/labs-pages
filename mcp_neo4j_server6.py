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
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    print("NEO4J_URI", "NEO4J_USER", "NEO4J_PASSWORD")
    print(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    try:
        with driver.session() as session:
            print(f"Eseguendo query: {query}")
            
            # 1️⃣ Esegui la query principale (lettura)
            result = session.execute_read(query)
            records = [record.data() for record in result]
            
            # 2️⃣ Crea un nodo per registrare la query eseguita usando una write transaction
            def create_query_node(tx):
                tx.run("CREATE (q:ExecutedQuery {query: $query})", query=query)
            session.execute_write(create_query_node)

            print("Query eseguita e registrata con successo.")
            return records
    finally:
        driver.close()

# Avvia il server con streamable HTTP (compatibile col client Strands)
if __name__ == "__main__":
    print("MCP Neo4j server in esecuzione su http://localhost:8000/mcp")
    mcp.run(transport="streamable-http")
