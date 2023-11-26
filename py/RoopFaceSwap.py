import cv2
import os
import torch
import numpy as np
from .scripts.swapper import getFaceSwapModel,get_face_single
from .third_part.GFPGAN.gfpgan import GFPGANer
from PIL import Image
import folder_paths

class RoopFaceSwap:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"template_image": ("IMAGE", ),
                    "user_image": ("IMAGE", ),
                    "facerestore": ([ True, False ], ),
                    },
                }

    CATEGORY = "lam"

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("图片",)

    FUNCTION = "swap_face"

    def swap_face(self,template_image,user_image,facerestore):
        face_swapper = getFaceSwapModel(folder_paths.models_dir+'/roop-face-swap/inswapper_128.onnx')
        if facerestore:
            restorer_model = GFPGANer(model_path=os.path.join(folder_paths.models_dir+'/upscale_models','GFPGANv1.4.pth'), upscale=1, arch='clean',
                                channel_multiplier=2, bg_upsampler=None)

        imaget_np=template_image.numpy()
        imageu_np=user_image.numpy()
        imgt_shape=imaget_np.shape
        imau_shape=imageu_np.shape
        if imgt_shape[0]<=0 or imau_shape[0]<=0:
            return (template_image,)

        sample_frames = []
        imageu=imageu_np[0]*255
        imageu=np.uint8(imageu)
        source_face = get_face_single(imageu, face_index=0)
        for i in range(imgt_shape[0]):
            imaget=imaget_np[i]*255
            imaget=np.uint8(imaget)
            target_face = get_face_single(imaget, face_index=0)
            if target_face is not None and source_face is not None:
                image = face_swapper.get(imaget, target_face, source_face)
            else:
                image = imaget
            #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            if facerestore:
                _,_,rimage=restorer_model.enhance(image)
                if rimage is not None:
                    image=rimage
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]
            image = image.squeeze()
            sample_frames.append(image)

        return (torch.stack(sample_frames),)

NODE_CLASS_MAPPINGS = {
    "RoopFaceSwap": RoopFaceSwap
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "RoopFaceSwap": "人脸替换"
}
