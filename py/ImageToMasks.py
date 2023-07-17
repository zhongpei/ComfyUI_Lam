
class ImageToMasks:
    @classmethod
    def INPUT_TYPES(s):
        return {
                "required": {
                    "image": ("IMAGE",),
                    "channel": (["red", "green", "blue"],),
                }
        }

    CATEGORY = "mask"

    RETURN_TYPES = ("MASK",)
    FUNCTION = "image_to_mask"

    def image_to_mask(self, image, channel):
        channels = ["red", "green", "blue"]
        mask = image[:, :, :, channels.index(channel)]
        return (mask,)

NODE_CLASS_MAPPINGS = {
    "ImageToMasks": ImageToMasks
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageToMasks": "图片转mask批量"
}