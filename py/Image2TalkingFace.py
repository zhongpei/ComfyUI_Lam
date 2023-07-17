import folder_paths
import cv2
import os
import torch
import numpy as np
from ffmpy import FFmpeg
from custom_nodes.ComfyUI_Lam.src.gradio_demo import SadTalker  

class Image2TalkingFace:
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
                        "images": ("IMAGE", ),
                        "audioPath": ("STRING", {"forceInput": True}),
                        "pose_style": ("INT", {"default": 0, "min": 0, "max": 64}),
                        "size_of_image": ([256, 512], ),
                        "preprocess_type":(['crop', 'resize','full', 'extcrop', 'extfull'], ),
                        "is_still_mode": ([ False, True ], ),
                        "batch_size": ("INT", {"default": 1, "min": 1, "max": 10}),
                        "enhancer": ([ False, True ], ),
                    },
                }

    CATEGORY = "lam"

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("视频文件名",)
    FUNCTION = "sad_talker"
    OUTPUT_NODE = True

    def sad_talker(self, images,audioPath,pose_style,size_of_image,preprocess_type,is_still_mode,batch_size,enhancer):
        sad_talker = SadTalker(self.checkpoint_path, "custom_nodes/ComfyUI_Lam/src/config", lazy_load=True)
        autio_path=sad_talker.test(images, audioPath,preprocess_type,is_still_mode,enhancer,batch_size,size_of_image,pose_style,result_dir=self.output_dir)
        return {"ui": {"text": "视频合成成功，保存路径："+autio_path}, "result": (autio_path,)}

NODE_CLASS_MAPPINGS = {
    "Image2TalkingFace": Image2TalkingFace
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "Image2TalkingFace": "图像转说话的人脸动画"
}
