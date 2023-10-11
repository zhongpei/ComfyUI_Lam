import folder_paths
import cv2
import os
import torch
import numpy as np
import imageio

class Image2Video:
    def __init__(self):
        self.output_dir = os.path.join(folder_paths.get_output_directory(), 'video')
        if not os.path.exists(self.output_dir):
            os .makedirs(self.output_dir)

    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"images": ("IMAGE", ),
                    "fps": ("INT", {"default": 20, "min": 1, "max": 100000}),
                    "img_frame_size": ("INT", {"default": 1, "min": 1, "max": 100000}),
                    "filename_prefix": ("STRING", {"default": "comfyUI"})},
                }

    CATEGORY = "lam"

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("视频文件名",)
    FUNCTION = "img2video"
    OUTPUT_NODE = True
    #OUTPUT_IS_LIST = (True,)
    
    def img2video(self, images,fps,img_frame_size,filename_prefix):
        imaget_np=images.numpy()
        imgt_shape=imaget_np.shape
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])
        file = f"{filename}_{counter:05}_.mp4"
        with imageio.get_writer(os.path.join(full_output_folder, file), fps=fps) as video:
            for i in range(imgt_shape[0]):
                imaget=np.uint8(imaget_np[i]*255)
                for n in range(img_frame_size):
                    video.append_data(imaget)# 写入视频
        return {"ui": {"text": "视频保存成功文件地址："+os.path.join(full_output_folder, file),
        'videos':[{'filename':file,'type':'output','subfolder':'video'}]}, "result": (os.path.join(full_output_folder, file),)}

NODE_CLASS_MAPPINGS = {
    "Image2Video": Image2Video
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "Image2Video": "图片转视频"
}
