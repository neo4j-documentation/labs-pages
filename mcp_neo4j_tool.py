from strands.types.tools import AgentTool
from neo4j import GraphDatabase
from datetime import timedelta
from strands.tools.mcp.mcp_client import MCPClient, MCPToolResult

class MCPNeo4jTool(AgentTool):
    """Tool MCP per eseguire query Neo4j reali."""

    def __init__(self, name: str, uri: str, user: str, password: str):
        super().__init__(name=name)
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def call(self, arguments: dict, read_timeout_seconds: timedelta | None = None) -> MCPToolResult:
        query = arguments.get("query")
        if not query:
            return MCPToolResult(
                status="error",
                toolUseId=arguments.get("toolUseId", "unknown"),
                content=[{"text": "Missing 'query' argument"}]
            )

        try:
            with self.driver.session() as session:
                result = session.run(query)
                records = [dict(r) for r in result]
            return MCPToolResult(
                status="success",
                toolUseId=arguments.get("toolUseId", "neo4j_tool"),
                content=[{"text": str(records)}]
            )
        except Exception as e:
            return MCPToolResult(
                status="error",
                toolUseId=arguments.get("toolUseId", "neo4j_tool"),
                content=[{"text": f"Neo4j query failed: {str(e)}"}]
            )
