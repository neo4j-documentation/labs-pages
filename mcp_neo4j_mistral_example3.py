from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.tools.mcp.mcp_client import MCPClient
from strands.models.mistral import MistralModel

def create_streamable_http_transport():
    return streamablehttp_client("http://localhost:8000/mcp/")

def main():
    # 1) Costruisci il client MCP
    streamable_http_mcp_client = MCPClient(create_streamable_http_transport)

    with streamable_http_mcp_client:
        # 2) Lista tools disponibili
        tools = streamable_http_mcp_client.list_tools_sync()
        print("TOOLS disponibili:", [t.mcp_tool.name for t in tools])

        # 3) Crea l'agente con Mistral
        agent = Agent(
            tools=tools,
            model=MistralModel(
                api_key="aDHQXyGQcIP4uNSdI6vc24YA8vjkLr22",
                model_id="mistral-small-latest",
                max_tokens=200,
                temperature=0.7
            )
        )

        # 4) Prompt strutturato: forza l'uso del tool
        prompt = """
You must always use the 'neo4j_query' tool to execute any query.
Do not calculate arithmetic yourself.
Query to execute: RETURN 125 + 375 AS result
"""
        response = agent(prompt)
        print("Risposta agente:", response)

        # 5) Chiamata diretta al tool (opzionale)
        result = streamable_http_mcp_client.call_tool_sync(
            tool_use_id="tool-1",
            name="neo4j_query",
            arguments={"query": "RETURN 125 + 375 AS result"}
        )
        print("Risultato Neo4j:", result)

if __name__ == "__main__":
    main()
