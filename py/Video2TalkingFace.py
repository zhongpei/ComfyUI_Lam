import folder_paths
import cv2
import os
import torch
import numpy as np
from custom_nodes.ComfyUI_Lam.src.gradio_demo import SadTalker  

class Video2TalkingFace:
    def __init__(self):
        self.output_dir = os.path.join(folder_paths.get_output_directory(), 'video')
        self.checkpoint_path=os.path.join(folder_paths.models_dir, 'SadTalker')
        if not os.path.exists(self.output_dir):
            os .makedirs(self.output_dir)
        if not os.path.exists(self.checkpoint_path):
            os .makedirs(self.checkpoint_path)
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {
                        "videoPath": ("STRING", {"forceInput": True}),
                        "audioPath": ("STRING", {"forceInput": True}),
                        "batch_size": ("INT", {"default": 1, "min": 1, "max": 10}),
                        "enhancer": ([ 'none','lip','face' ], ),
                    },
                }

    CATEGORY = "lam"

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("视频文件名",)
    FUNCTION = "sad_talker"
    OUTPUT_NODE = True

    def sad_talker(self, videoPath,audioPath,batch_size,enhancer):
        sad_talker = SadTalker(self.checkpoint_path, "custom_nodes/ComfyUI_Lam/src/config", lazy_load=True)
        autio_path=sad_talker.run_video_2_video(videoPath,audioPath,enhancer,batch_size,result_dir=self.output_dir)
        return {"ui": {"text": "视频合成成功，保存路径："+autio_path}, "result": (autio_path,)}

NODE_CLASS_MAPPINGS = {
    "Video2TalkingFace": Video2TalkingFace
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "Video2TalkingFace": "视频转说话的人脸动画"
}
