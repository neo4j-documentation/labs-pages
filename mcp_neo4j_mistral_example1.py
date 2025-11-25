# mcp_neo4j_mistral_example.py

from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.tools.mcp.mcp_client import MCPClient
from strands.models.mistral import MistralModel

def create_streamable_http_transport():
    # URL del tuo server FastMCP
    return streamablehttp_client("http://localhost:8000/mcp/")

def main():
    # 1️⃣ Costruisci il client MCP
    streamable_http_mcp_client = MCPClient(create_streamable_http_transport)

    with streamable_http_mcp_client:
        # 2️⃣ Lista dei tool disponibili
        tools = streamable_http_mcp_client.list_tools_sync()
        print("TOOLS disponibili:", [getattr(t, "name", t.mcp_tool.name) for t in tools])

        # 3️⃣ Crea l'agente con modello Mistral
        agent = Agent(
            tools=tools,
            model=MistralModel(
                api_key="aDHQXyGQcIP4uNSdI6vc24YA8vjkLr22",  # <--- metti la tua chiave
                model_id="mistral-small-latest",
                max_tokens=200,
                temperature=0.7,
            )
        )

        # 4️⃣ Esempio: Mistral usa il tool neo4j_query per calcolare 125+375
        # Nota: il prompt deve istruire l'agente a usare il tool
        prompt = """
        Compute 125 + 375 using the neo4j_query tool.
        Only use the tool, do not calculate in your head.
        """

        response = agent(prompt)
        print("Risposta agente:", response)

        # 5️⃣ Alternativa: chiamata diretta al tool (manuale)
        cypher_query = "RETURN 125 + 375 AS result"
        result = streamable_http_mcp_client.call_tool_sync(
            tool_use_id="tool-1",
            name="neo4j_query",
            arguments={"query": cypher_query}
        )
        print("Risultato Neo4j:", result["content"][0]["text"])

if __name__ == "__main__":
    main()
