from PIL import Image
import numpy as np
import torch
import os
import folder_paths

class VideoPath:
    def __init__(self):
        self.input_video_dir = os.path.join(folder_paths.get_input_directory(), 'video')
        if not os.path.exists(self.input_video_dir):
            os .makedirs(self.input_video_dir)

    @classmethod
    def INPUT_TYPES(cls):
        input_video_dir = os.path.join(folder_paths.get_input_directory(), 'video')
        if not os.path.exists(input_video_dir):
            os .makedirs(input_video_dir)
        files = [f for f in os.listdir(input_video_dir) if os.path.isfile(os.path.join(input_video_dir, f))]
        return {
            "required": {
                "video": (sorted(files), ),
            }
        }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("视频地址",)
    FUNCTION = "get_video_path"

    CATEGORY = "lam"

    def get_video_path(self,video):
        video_path = folder_paths.get_annotated_filepath(video,self.input_video_dir)
        return (video_path, )

NODE_CLASS_MAPPINGS = {
    "VideoPath": VideoPath
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoPath": "获取视频地址"
}
