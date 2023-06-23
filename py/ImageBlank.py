from PIL import Image
import numpy as np
import torch
class ImageBlank:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "count": ("INT", {"default": 1, "min": 1, "max": 99999, "step": 1}),
                "width": ("INT", {"default": 512, "min": 8, "max": 4096, "step": 1}),
                "height": ("INT", {"default": 512, "min": 8, "max": 4096, "step": 1}),
                "red": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1}),
                "green": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1}),
                "blue": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1}),
            }
        }
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "blank_image"

    CATEGORY = "lam"

    def blank_image(self,count, width, height, red, green, blue):

        # Ensure multiples
        width = (width // 8) * 8
        height = (height // 8) * 8
        images=[]
        for i in range(count):
            # Blend image
            image = Image.new(mode="RGB", size=(width, height),
                            color=(red, green, blue))
            images.append(torch.from_numpy(np.array(image).astype(np.float32) / 255.0))

        return (torch.stack(images), )

NODE_CLASS_MAPPINGS = {
    "ImageBlank": ImageBlank
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageBlank": "创建空图片"
}
