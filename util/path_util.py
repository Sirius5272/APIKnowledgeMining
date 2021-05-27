from pathlib import Path
from definitions import DATA_DIR, OUTPUT_DIR


class PathUtil:
    @classmethod
    def post_data_json(cls, filename="post_data.json"):
        path = Path(DATA_DIR)
        path.mkdir(exist_ok=True)
        return str(path / "{filename}".format(filename=filename))

