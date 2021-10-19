from component.kg.model import APIKnowledgeKG
from util.path_util import PathUtil


if __name__ == "__main__":
    kg_path = PathUtil.api_knowledge_kg()
    kg: APIKnowledgeKG = APIKnowledgeKG.load(kg_path)
    #kg.print_simple()

    res = kg.get_instances_by_api("java.util.Scanner")
    for each in res:
        print(each)
