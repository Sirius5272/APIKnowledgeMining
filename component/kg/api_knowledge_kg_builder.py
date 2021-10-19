from component.model.snowball_result import SnowBallResult
from component.kg.model import APIKnowledgeKG


class KGBuilder:

    def build_kg(self, snowball_result: SnowBallResult) -> APIKnowledgeKG:
        kg = APIKnowledgeKG(snowball_result)
        kg.build_api_2_knowledge_map()
        kg.build_api_2_instance_map()
        return kg
