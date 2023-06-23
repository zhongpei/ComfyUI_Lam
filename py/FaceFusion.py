import cv2
import os
import torch
import numpy as np
from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from PIL import Image

class FaceFusion:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"template_image": ("IMAGE", ),
                    "user_image": ("IMAGE", )},
                }

    CATEGORY = "lam"

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("图片",)

    FUNCTION = "face_fusion"
    def face_fusion(self,template_image,user_image):
        image_face_fusion = pipeline(Tasks.image_face_fusion, model='damo/cv_unet-image-face-fusion_damo')
        imaget_np=template_image.numpy()
        imageu_np=user_image.numpy()
        imgt_shape=imaget_np.shape
        imau_shape=imageu_np.shape
        if imgt_shape[0]<=0 or imau_shape[0]<=0:
            return (template_image,)

        sample_frames = []
        imageu=imageu_np[0]*255
        imageu=Image.fromarray(np.uint8(imageu))
        for i in range(imgt_shape[0]):
            imaget=imaget_np[i]*255
            imaget=Image.fromarray(np.uint8(imaget))
            result = image_face_fusion(dict(template=imaget, user=imageu))
            image = result[OutputKeys.OUTPUT_IMG]
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]
            image = image.squeeze()
            sample_frames.append(image)

        return (torch.stack(sample_frames),)

NODE_CLASS_MAPPINGS = {
    "FaceFusion": FaceFusion
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "FaceFusion": "脸部融合"
}
