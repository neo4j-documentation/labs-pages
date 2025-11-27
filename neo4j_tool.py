# neo4j_tool.py
from neo4j import GraphDatabase

class MCPNeo4jTool:
    """MCP tool for executing Neo4j queries"""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.name = "neo4j_tool"

    def run(self, input_data: dict):
        """Executes the Neo4j query provided as input_data['query']"""
        query = input_data.get("query")
        if not query:
            return {"error": "No query provided"}

        with self.driver.session() as session:
            result = session.run(query)
            rows = [record.data() for record in result]
        return {"result": rows}
