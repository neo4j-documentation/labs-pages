from mcp.client.streamable_http import streamablehttp_client
from mcp.client import MCPClient

def create_transport():
    return streamablehttp_client("http://localhost:8000/mcp")

if __name__ == "__main__":
    client = MCPClient(create_transport)
    with client:
        tools = client.list_tools_sync()
        print("TOOLS disponibili dal server MCP:", [t.name for t in tools])

        # Esegui una query di test su Neo4j
        query = "MATCH (n) RETURN n LIMIT 5"
        result = client.call_sync("neo4j_query", query)
        print("RISULTATO QUERY:\n", result)
