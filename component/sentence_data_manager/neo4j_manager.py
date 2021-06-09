from py2neo import Graph, Relationship, NodeMatcher
from util.tool import Tool
from util.path_util import PathUtil
import tqdm


class APIDataManager:
    def __init__(self):
        self.graph = None

    def connect_neo4j(self):
        self.graph = Graph(
            "http://106.14.239.166:17474/db/data/",
            user="neo4j",
            password="123456"

        )

    def node_match(self):
        matcher = NodeMatcher(self.graph)
        result = matcher.match("entity", api_id=85).all()
        return result


if __name__ == "__main__":
    manager = APIDataManager()
    manager.connect_neo4j()
    name_list = []
    print("matching node")
    node_list = manager.node_match()
    print("finish match node")
    for node in tqdm.tqdm(node_list):
        tmp_dict = {
            "qualified_name": node["qualified_name"],
            "alias": node["alias"],
            "short_name": node["short_name"],
            "long_name": node["long_name"]
        }
        name_list.append(tmp_dict)
    Tool.write_list_to_json(name_list, PathUtil.api_name_json())
