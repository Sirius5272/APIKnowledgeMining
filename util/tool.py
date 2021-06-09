import json


class Tool:
    @classmethod
    def write_list_to_json(cls, data, file_name):
        json_obj = json.dumps(data, indent=4)
        file_object = open(file_name, 'w')
        file_object.write(json_obj)
        file_object.close()
