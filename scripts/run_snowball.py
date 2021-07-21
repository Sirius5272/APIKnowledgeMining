from component.snowball import Snowball
from util.data_util import DataUtil
from util.path_util import PathUtil


class RunSnowball:
    @classmethod
    def run(cls):
        snowball = Snowball()
        seed_api_knowledge_list = DataUtil.seed_api_knowledge_data()
        seed_sentence_list = DataUtil.seed_sentence_data()
        sentence_list = DataUtil.sentence_data(PathUtil.filtered_sentence_dict(score=0.999))
        new_list = []
        new_list.extend(seed_sentence_list)
        new_list.extend(sentence_list)
        new_list = list(set(new_list))
        snowball.run(seed_api_knowledge_list=seed_api_knowledge_list,
                     sentence_list=new_list,
                     max_step=4,
                     save_by_step=2,
                     seed_selector_path=PathUtil.seed_selector(),
                     previous_snowball_result_path=PathUtil.snowball_result(),
                     output_path=PathUtil.snowball_result()
                     )


if __name__ == "__main__":
    RunSnowball.run()
