# mcp_client_example_mistral.py

from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.tools.mcp.mcp_client import MCPClient

# IMPORT MISTRAL MODEL
from strands.models.mistral import MistralModel
import os
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

def create_streamable_http_transport():
    # The URL must be the one of your FastMCP server
    return streamablehttp_client("http://localhost:8000/mcp/")


def main():
    # 1) Create the MCP client
    streamable_http_mcp_client = MCPClient(create_streamable_http_transport)

    with streamable_http_mcp_client:
        # 2) List available MCP tools
        tools = streamable_http_mcp_client.list_tools_sync()
        print("Available TOOLS:", [getattr(t, "name", t.mcp_tool.name) for t in tools])

        # 3) Create the agent using Mistral
        agent = Agent(
            tools=tools,
            model=MistralModel(
                api_key=MISTRAL_API_KEY,
                model_id="mistral-small-latest",
                temperature=0.7,
                max_tokens=200,
            ),
        )

        # 4) Ask a question through the agent
        response = agent("What is 125 plus 375?")
        print("Agent response:", response)

        # 5) Or directly call a tool
        result = streamable_http_mcp_client.call_tool_sync(
            tool_use_id="tool-1",
            name="neo4j_query",
            arguments={"x": 125, "y": 375},
        )
        print("Calculator result:", result["content"][0]["text"])


if __name__ == "__main__":
    main()
