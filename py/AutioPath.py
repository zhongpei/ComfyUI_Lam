from PIL import Image
import numpy as np
import torch
import folder_paths
import os
class AutioPath:
    def __init__(self):
        self.input_autio_dir = os.path.join(folder_paths.get_input_directory(), 'autio')
        if not os.path.exists(self.input_autio_dir):
            os .makedirs(self.input_autio_dir)

    @classmethod
    def INPUT_TYPES(cls):
        input_autio_dir = os.path.join(folder_paths.get_input_directory(), 'autio')
        if not os.path.exists(input_autio_dir):
            os .makedirs(input_autio_dir)
        autiofiles = [f for f in os.listdir(input_autio_dir) if os.path.isfile(os.path.join(input_autio_dir, f))]
        return {
            "required": {
                "autio": (sorted(autiofiles), ),
            }
        }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("音频地址",)
    FUNCTION = "get_autio_path"

    CATEGORY = "lam"

    def get_autio_path(self,autio):
        autio_path = folder_paths.get_annotated_filepath(autio,self.input_autio_dir)
        return (autio_path, )

NODE_CLASS_MAPPINGS = {
    "AutioPath": AutioPath
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "AutioPath": "获取音频地址"
}
