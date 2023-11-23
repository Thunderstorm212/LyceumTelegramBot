import json
import os


class ChatData:

    def __init__(self):
        self.path_file = "conf/chats_data.json"
        self.chat_data_file = open(self.path_file)

    def add(self, obj_id: str, input_data):
        file_data = dict(json.load(self.chat_data_file))
        obj_id = obj_id.split(".")

        def change_value(obj, target_key, new_value):
            for key in obj:
                if key == target_key:
                    obj[key] = new_value
                elif isinstance(obj[key], dict):
                    change_value(obj[key], target_key, new_value)

        change_value(file_data[obj_id[0]], obj_id[-1], input_data)
        json_file = json.dumps(file_data, sort_keys=True, indent=2, ensure_ascii=False)
        open(self.path_file, "w+").write(json_file)

    def add_obj(self, input_data: dict):
        file_data = dict(json.load(self.chat_data_file))
        print("file data", file_data)
        for key, val in input_data.items():
            file_data[key] = val

        json_file = json.dumps(file_data, sort_keys=True, indent=2, ensure_ascii=False)
        open(self.path_file, "w+").write(json_file)

    def get(self):
        return json.load(self.chat_data_file)

    def get_by_id(self, obj_id: str):
        file_data = dict(json.load(self.chat_data_file))
        obj_id = obj_id.split(".")
        try:
            for key in obj_id:
                file_data = file_data[key]
            return file_data
        except (KeyError, TypeError):
            return None

    def get_ides(self):
        file_data = dict(json.load(self.chat_data_file))
        ides = []
        for i in file_data.keys():
            ides.append(i)
        return ides

