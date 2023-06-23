import math
import torch
import comfy.utils
import numpy as np
import cv2

class LoadReplaceImage:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"image_t": ("IMAGE", ),
                    "mask": ("MASK",),
                    "grow_mask_by": ("INT", {"default": 6, "min": 0, "max": 64, "step": 1}),
                    "image_bt": ("IMAGE", ),},
                }

    CATEGORY = "lam"

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("图片",)
    FUNCTION = "load_replace_image"
    def load_replace_image(self, image_t,mask,grow_mask_by,image_bt):
        if grow_mask_by == 0:
            mask_erosion = mask
        else:
            grow_mask_by=grow_mask_by+1 if grow_mask_by%2==0 else grow_mask_by
            kernel_tensor = torch.ones((1, 1, grow_mask_by, grow_mask_by))
            padding = math.ceil((grow_mask_by - 1) / 2)
            mask_erosion = torch.clamp(torch.nn.functional.conv2d(mask.round(), kernel_tensor, padding=padding), 0, 1)

        if image_t.shape != image_bt.shape:
            image_bt = image_bt.permute(0, 3, 1, 2)
            image_bt = comfy.utils.common_upscale(image_bt, image_t.shape[2], image_t.shape[1], upscale_method='bicubic', crop='center')
            image_bt = image_bt.permute(0, 2, 3, 1)
        
        replace_image = self.blend_mode(image_t, image_bt, mask_erosion)
        return (replace_image,)

    def blend_mode(self, img1, img2, mask):
        mask_np=mask.numpy()
        mask_shape=mask_np.shape
        img_shape=img2.size()
        if tuple(mask_shape)!=tuple(img_shape):
            maskList=[]
            for i in range(mask_shape[0]):
                maskList.append(cv2.resize(mask_np[i],(img_shape[2],img_shape[1])))
            mask_np=np.array(maskList)
            mask_shape=mask_np.shape
        mask_np_rgb = np.zeros((mask_shape[0],mask_shape[1],mask_shape[2],3))
        mask_np_rgb[:,:,:,0] = mask_np
        mask_np_rgb[:,:,:,1] = mask_np
        mask_np_rgb[:,:,:,2] = mask_np
        
        mask=torch.from_numpy(mask_np_rgb)
        print("-----------",mask.size())
        print("-----------",img1.size())
        print("-----------",img2.size())
        if tuple(mask.size())!=tuple(img1.size()) or tuple(img1.size())!=tuple(img2.size()):
            return img2
        img1=img1*mask
        img2=img2*(1-mask)
        return img1+img2


NODE_CLASS_MAPPINGS = {
    "LoadReplaceImage": LoadReplaceImage
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadReplaceImage": "图片局部替换"
}
