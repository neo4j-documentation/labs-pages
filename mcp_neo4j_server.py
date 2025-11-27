from mcp.server import FastMCP
from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError
import os

# Neo4j configuration
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "apoc12345")

# Create the MCP server
mcp = FastMCP("Neo4j MCP Server")

@mcp.tool(description="Execute a Neo4j query, return the result, and log the query")
def neo4j_query(query: str):
    try:
        with GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)) as driver:
            print(f"[LOG] Attempting connection to Neo4j with URI: {NEO4J_URI}, user: {NEO4J_USER}")

            try:
                with driver.session() as session:
                    # 1️⃣ Read query
                    def run_main_query(tx):
                        print(f"[LOG] Executing main query: {query}")
                        result = tx.run(query)
                        records = [record.data() for record in result]  # ✅ here
                        print(f"[LOG] Query results: {records}")
                        return records

                    records = session.execute_read(run_main_query)

                    session.run(
                        "CREATE (q:ExecutedQuery) SET q.executedQuery = $query RETURN q",
                        parameters={"query": query}
                    ).single()

                    print("[LOG] Query executed and logged successfully.")
                    return records

            except Neo4jError as e:
                print(f"[ERROR] Error executing query: {e}")
                return {"error": str(e)}

    except Neo4jError as e:
        print(f"[ERROR] Error executing query: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    print("MCP Neo4j server running at http://localhost:8000/mcp")
    mcp.run(transport="streamable-http")
