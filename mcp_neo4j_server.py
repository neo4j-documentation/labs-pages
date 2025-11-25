from mcp.server import FastMCP
from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError
import os

# Configurazione Neo4j
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "apoc12345")

# Crea il server MCP
mcp = FastMCP("Neo4j MCP Server")

@mcp.tool(description="Esegui una query Neo4j, ritorna il risultato e registra la query")
def neo4j_query(query: str):
    try: 
        with GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)) as driver:
            print(f"[LOG] Tentativo di connessione a Neo4j con URI: {NEO4J_URI}, utente: {NEO4J_USER}")

            try:
                with driver.session() as session:
                    # 1️⃣ Lettura query
                    def run_main_query(tx):
                        print(f"[LOG] Esecuzione query principale: {query}")
                        result = tx.run(query)
                        records = [record.data() for record in result]  # ✅ qui dentro
                        print(f"[LOG] Risultati query: {records}")
                        return records

                    records = session.execute_read(run_main_query)

                    session.run(
                        "CREATE (q:ExecutedQuery) SET q.executedQuery = $query RETURN q",
                        parameters={"query": query}
                    ).single()

                    print("[LOG] Query eseguita e registrata con successo.")
                    return records

            except Neo4jError as e:
                print(f"[ERRORE] Durante l'esecuzione della query: {e}")
                return {"error": str(e)}

            # finally:
            #     # driver.close()
            #     print("[LOG] Connessione Neo4j chiusa.")
            #         # 2️⃣ Scrittura nodo
            #         # def create_query_node(tx):
            #         #     tx.run("CREATE (q:ExecutedQuery {query: $query})", query=query).consume()
            #         #     print(f"[LOG] Nodo registrato per la query: {query}")

            # try:
            #     with driver.session() as session:
            #         # create node and set the query property using a parameter
            #         session.run(
            #             "CREATE (q:ExecutedQuery) SET q.query = $query RETURN q",
            #             parameters={"query": query}
            #         ).single()

            #         print("[LOG] Query eseguita e registrata con successo.")
            #         # return records

            # except Neo4jError as e:
            #     print(f"[ERRORE] Durante l'esecuzione della query: {e}")
            #     return {"error": str(e)}

            # finally:
            #     # driver.close()
            #     print("[LOG] Connessione Neo4j chiusa.")
            # driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
            

            # try:
            #     # Verifica connessione
            #     try:
            #         with driver.session() as session:
            #             session.run("RETURN 1").single()
            #         print("[LOG] Connessione a Neo4j stabilita con successo.")
            #     except Neo4jError as e:
            #         print(f"[ERRORE] Connessione a Neo4j fallita: {e}")
            #         return {"error": str(e)}

            #     with driver.session() as session:

            #         # Esegui query principale in lettura
            #         def run_main_query(tx):
            #             print(f"[LOG] Esecuzione query principale: {query}")
            #             return tx.run(query)

            #         result = session.execute_read(run_main_query)
            #         records = [record.data() for record in result]
            #         print(f"[LOG] Risultati query: {records}")

            #         # Registra la query come nodo in scrittura
            #         def create_query_node(tx):
            #             tx.run("CREATE (q:ExecutedQuery {query: $query})", query=query)
            #             print(f"[LOG] Nodo registrato per la query: {query}")

            #         session.execute_write(create_query_node)

            #         print("[LOG] Query eseguita e registrata con successo.")
            #         return records

            # except Neo4jError as e:
            #     print(f"[ERRORE] Durante l'esecuzione della query: {e}")
            #     return {"error": str(e)}

            # finally:
            #     driver.close()
            #     print("[LOG] Connessione Neo4j chiusa.")
    except Neo4jError as e:
        print(f"[ERRORE] Durante l'esecuzione della query: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    print("MCP Neo4j server in esecuzione su http://localhost:8000/mcp")
    mcp.run(transport="streamable-http")
