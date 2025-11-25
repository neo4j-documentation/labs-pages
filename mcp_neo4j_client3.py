# mcp_client_example.py

from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.tools.mcp.mcp_client import MCPClient

def create_streamable_http_transport():
    # Nota: l'URL deve corrispondere a quello usato dal tuo server FastMCP
    return streamablehttp_client("http://localhost:8000/mcp/")

def main():
    # Costruisci il client MCP di Strands
    streamable_http_mcp_client = MCPClient(create_streamable_http_transport)

    # Usa il client in un context manager
    with streamable_http_mcp_client:
        tools = streamable_http_mcp_client.list_tools_sync()
        print("TOOLS disponibili:", [getattr(t, "name", t.mcp_tool.name) for t in tools])

        # Crea l'agente Strands con quegli strumenti
        agent = Agent(tools=tools)

        # Chiedi qualcosa all'agente che usa il tool "add"
        response = agent("What is 125 plus 375?")
        print("Risposta agente:", response)

        # Oppure invoca direttamente il tool
        result = streamable_http_mcp_client.call_tool_sync(
            tool_use_id="tool-1",
            name="add",
            arguments={"x": 125, "y": 375}
        )
        print("Risultato calcolatore:", result["content"][0]["text"])

if __name__ == "__main__":
    main()
