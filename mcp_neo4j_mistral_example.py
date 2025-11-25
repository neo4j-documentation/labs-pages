from strands import Agent
from mcp.client.streamable_http import streamablehttp_client
from strands.tools.mcp.mcp_client import MCPClient
from strands.models.mistral import MistralModel

def create_streamable_http_transport():
    return streamablehttp_client("http://localhost:8000/mcp/")

def main():
    mcp_client = MCPClient(create_streamable_http_transport)
    
    with mcp_client:
        tools = mcp_client.list_tools_sync()
        print("TOOLS disponibili:", [getattr(t, "name", t.mcp_tool.name) for t in tools])

        # Agente Mistral con prompt system che forza l'uso del tool
        agent = Agent(
            tools=tools,
            model=MistralModel(
                api_key="aDHQXyGQcIP4uNSdI6vc24YA8vjkLr22",
                model_id="mistral-small-latest",
                max_tokens=200,
                temperature=0,
                stream=False
            ),
            system_prompt=(
                "Se ricevi un'operazione da eseguire, non calcolarla da solo. "
                "Usa sempre il tool Neo4j `neo4j_query` per ottenere il risultato. "
                "Non scrivere numeri direttamente, sempre tramite il tool."
            )
        )

        # Esempio: somma tramite query Neo4j
        query = "RETURN 125 + 375 AS result"
        response = agent(f"Esegui la query: {query}")
        print("Risposta agente:", response)

if __name__ == "__main__":
    main()
