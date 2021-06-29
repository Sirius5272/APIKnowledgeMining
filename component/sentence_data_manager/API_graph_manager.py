from sekg.graph.exporter.graph_data import GraphData
from util.path_util import PathUtil
from util.tool import Tool


class APIGraphManager:
    graph: GraphData = None

    def __init__(self, graph):
        if not self.graph:
            self.graph = graph

    def get_api_name_from_graph(self):
        method_id_list = list(self.graph.get_node_ids_by_label("method"))
        class_id_list = list(self.graph.get_node_ids_by_label("class"))
        interface_id_list = list(self.graph.get_node_ids_by_label("interface"))
        package_id_list = list(self.graph.get_node_ids_by_label("package"))
        node_id_list = []
        node_id_list.extend(method_id_list)
        node_id_list.extend(class_id_list)
        node_id_list.extend(interface_id_list)
        node_id_list.extend(package_id_list)
        node_id_list = list(set(node_id_list))
        api_name_list = {}

        for node_id in node_id_list:
            node = self.graph.get_node_info_dict(node_id)

            qualified_name = node["properties"]["qualified_name"]
            api_name_list[qualified_name] = qualified_name
            if "." in qualified_name:
                short_name = qualified_name.split(".")[-1]
                api_name_list[short_name] = qualified_name

                if "(" in short_name:
                    short_name_without_param = short_name.split("(")[0]
                    api_name_list[short_name_without_param] = qualified_name

        Tool.write_list_to_json(api_name_list, PathUtil.api_name_from_jdk_graph())


if __name__ == "__main__":
    graph = GraphData.load(PathUtil.jdk_graph())
    manager = APIGraphManager(graph)
    manager.get_api_name_from_graph()

