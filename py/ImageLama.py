import math
import torch
import comfy.utils
import numpy as np
import cv2
from .lama import LamaInpainting

def pad64(x):
    return int(np.ceil(float(x) / 64.0) * 64 - x)


def safer_memory(x):
    # Fix many MAC/AMD problems
    return np.ascontiguousarray(x.copy()).copy()

def HWC3(x):
    assert x.dtype == np.uint8
    if x.ndim == 2:
        x = x[:, :, None]
    assert x.ndim == 3
    H, W, C = x.shape
    assert C == 1 or C == 3 or C == 4
    if C == 3:
        return x
    if C == 1:
        return np.concatenate([x, x, x], axis=2)
    if C == 4:
        color = x[:, :, 0:3].astype(np.float32)
        alpha = x[:, :, 3:4].astype(np.float32) / 255.0
        y = color * alpha + 255.0 * (1.0 - alpha)
        y = y.clip(0, 255).astype(np.uint8)
        return y


def resize_image_with_pad(input_image, resolution, skip_hwc3=False):
    if skip_hwc3:
        img = input_image
    else:
        img = HWC3(input_image)
    H_raw, W_raw, _ = img.shape
    k = float(resolution) / float(min(H_raw, W_raw))
    interpolation = cv2.INTER_CUBIC if k > 1 else cv2.INTER_AREA
    H_target = int(np.round(float(H_raw) * k))
    W_target = int(np.round(float(W_raw) * k))
    img = cv2.resize(img, (W_target, H_target), interpolation=interpolation)
    H_pad, W_pad = pad64(H_target), pad64(W_target)
    img_padded = np.pad(img, [[0, H_pad], [0, W_pad], [0, 0]], mode='edge')

    def remove_pad(x):
        return safer_memory(x[:H_target, :W_target])

    return safer_memory(img_padded), remove_pad

class ImageLama:

    def __init__(self,res=512):
        self.res=res
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"images": ("IMAGE", ),
                    "mask": ("MASK",),
                    },
                }

    CATEGORY = "lam"

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("图片",)
    FUNCTION = "lama_inpaint"
    def lama_inpaint(self, images,mask):
        mask_np=mask.numpy()
        mask_shape=mask_np.shape
        imaget_np=images.numpy()
        imgt_shape=imaget_np.shape
        prd_images=[]
        for i in range(imgt_shape[0]):
            imaget=np.uint8(imaget_np[i]*255)
            imaget = cv2.cvtColor(imaget, cv2.COLOR_BGR2RGB)
            mask=np.uint8(mask_np*255)
            mask=np.expand_dims(mask, axis=-1)
            H, W, C = imaget.shape
            img=np.zeros((H,W,4))
            img[:,:,0:3]=imaget
            img[:,:,3:4]=mask

            raw_color = img[:, :, 0:3].copy()
            raw_mask = img[:, :, 3:4].copy()

            res = 256  # Always use 256 since lama is trained on 256

            img_res, remove_pad = resize_image_with_pad(img, res, skip_hwc3=True)

            model_lama = LamaInpainting()

            # applied auto inversion
            prd_color = model_lama(img_res)
            prd_color = remove_pad(prd_color)
            prd_color = cv2.resize(prd_color, (W, H))

            alpha = raw_mask.astype(np.float32) / 255.0
            fin_color = prd_color.astype(np.float32) * alpha + raw_color.astype(np.float32) * (1 - alpha)
            fin_color = fin_color.clip(0, 255).astype(np.uint8)
            
            fin_color = cv2.cvtColor(fin_color, cv2.COLOR_BGR2RGB)
            prd_images.append(torch.from_numpy(np.array(fin_color).astype(np.float32) / 255.0))

        return (torch.stack(prd_images),)

    


NODE_CLASS_MAPPINGS = {
    "ImageLama": ImageLama
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageLama": "图片局部重绘lama"
}
