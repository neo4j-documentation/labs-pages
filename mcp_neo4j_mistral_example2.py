# mcp_neo4j_mistral_example.py

from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.tools.mcp.mcp_client import MCPClient
from strands.models.mistral import MistralModel


def create_transport():
    # Transport per comunicare col server MCP locale
    return streamablehttp_client("http://localhost:8000/mcp/")


def main():
    # 1️⃣ Configura client MCP
    client = MCPClient(create_transport)

    with client:
        # Lista tool disponibili
        tools = client.list_tools_sync()
        print("TOOLS disponibili:", [t.mcp_tool.name for t in tools])

        # 2️⃣ Crea l'agente Mistral
        # Nota: aggiungiamo al prompt istruzioni per usare solo i tool
        agent = Agent(
            tools=tools,
            model=MistralModel(
                api_key="aDHQXyGQcIP4uNSdI6vc24YA8vjkLr22",  # metti la tua chiave
                model_id="mistral-small-latest",
                max_tokens=200,
                temperature=0.0,
                system_prompt=(
                    "You are a Neo4j assistant. "
                    "You MUST always use the 'neo4j_query' tool to execute queries. "
                    "Never answer arithmetic yourself."
                )
            )
        )

        # 3️⃣ Prompt all'agente
        prompt = """
        You must always use the 'neo4j_query' tool to execute any query.
        Do not answer arithmetic yourself.

        Execute this query in Neo4j: RETURN 125 + 375 AS result
        """

        # Invocazione dell'agente
        response = agent(prompt)
        print("Risposta agente:", response)

        # 4️⃣ Chiamata diretta al tool Neo4j (solo per verifica)
        neo4j_result = client.call_tool_sync(
            tool_use_id="tool-1",
            name="neo4j_query",
            arguments={"query": "RETURN 125 + 375 AS result"}
        )
        print("Risultato Neo4j:", neo4j_result)


if __name__ == "__main__":
    main()
