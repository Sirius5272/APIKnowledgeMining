from component.kg.api_knowledge_kg_builder import KGBuilder
from component.model.snowball_result import SnowBallResult
from util.path_util import PathUtil


if __name__ == "__main__":
    builder = KGBuilder()
    snowball_result_path = PathUtil.snowball_result_after_filter()
    snowball_result: SnowBallResult = SnowBallResult.load(snowball_result_path)
    kg = builder.build_kg(snowball_result)
    kg.save(PathUtil.api_knowledge_kg())
    api_2_instance_list = kg.get_api_2_instance_number_list()
    for each in api_2_instance_list:
        print(each)
