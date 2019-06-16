import os
import random
from py2neo import Graph

### Connection to graph.
neo4jUrl = "bolt://localhost:7687"
graph = Graph(neo4jUrl, bolt=True, password='odproject')


### Cypher queries.
# querie="""
# """


### Execution of Cypher queries.
#graph.run()

