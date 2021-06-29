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

    def node_match(self, amount, time):
        matcher = NodeMatcher(self.graph)
        try:
            result = matcher.match("entity").limit(amount).skip(amount * time).all()
            return result
        except:
            return []


if __name__ == "__main__":
    manager = APIDataManager()
    manager.connect_neo4j()
    print("matching node")
    name_list = []
    for i in range(300, 1185):
        print("the " + str(i) + " times getting api name data")

        node_list = manager.node_match(10000, i)
        for node in tqdm.tqdm(node_list):
            tmp_dict = {
                "qualified_name": node["qualified_name"],
                "alias": node["alias"],
                "short_name": node["short_name"],
                "long_name": node["long_name"]
            }
            name_list.append(tmp_dict)

        if (i+1) % 10 == 0:
            Tool.write_list_to_json(name_list, PathUtil.api_name_json((i+1)/10))
            name_list.clear()
    print("finish match node")


