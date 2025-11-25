# neo4j_tool.py
from neo4j import GraphDatabase

class MCPNeo4jTool:
    """Tool MCP per eseguire query Neo4j"""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.name = "neo4j_tool"

    def run(self, input_data: dict):
        """Esegue query Neo4j passata come input_data['query']"""
        query = input_data.get("query")
        if not query:
            return {"error": "No query provided"}

        with self.driver.session() as session:
            result = session.run(query)
            rows = [record.data() for record in result]
        return {"result": rows}
