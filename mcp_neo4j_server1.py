# mcp_neo4j_server.py
import asyncio
from strands.tools.mcp import MCPServer
from neo4j_tool import MCPNeo4jTool

async def main():
    server = MCPServer()

    # Registra Neo4jTool
    neo4j_tool = MCPNeo4jTool(uri="bolt://localhost:7687", user="neo4j", password="password")
    server.register_tool(neo4j_tool)

    print("MCP Neo4j Server pronto con tool 'neo4j_tool'...")
    await server.start(host="0.0.0.0", port=8000)

if __name__ == "__main__":
    asyncio.run(main())
