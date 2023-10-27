from PIL import Image
import numpy as np
import torch
class ImageClone:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE", ),
                "clone_multiple": ("INT", {"default": 2, "min": 2, "max": 99999, "step": 1}),
            }
        }
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "blank_image"

    CATEGORY = "lam"

    def blank_image(self,images, clone_multiple):
        return (images.repeat(images.size()[0]*clone_multiple,1,1,1), )

NODE_CLASS_MAPPINGS = {
    "ImageClone": ImageClone
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageClone": "图片克隆"
}
