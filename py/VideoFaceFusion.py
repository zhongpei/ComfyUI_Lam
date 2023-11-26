import cv2
import os
import torch
import numpy as np
from .src.face_fusion.image_face_fusion import ImageFaceFusion
from .third_part.GFPGAN.gfpgan import GFPGANer
from PIL import Image
import folder_paths
from ffmpy import FFmpeg
import imageio
from tqdm import tqdm 

class VideoFaceFusion:
    def __init__(self):
        self.output_dir = os.path.join(folder_paths.get_output_directory(), 'video')
        if not os.path.exists(self.output_dir):
            os .makedirs(self.output_dir)

    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"templateVideoPath": ("STRING", {"forceInput": True}),
                    "user_image": ("IMAGE", ),
                    "filename_prefix": ("STRING", {"default": "comfyUI"}),
                    },
                }

    CATEGORY = "lam"

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("视频文件名",)
    OUTPUT_NODE = True

    FUNCTION = "face_fusion"
    def face_fusion(self,templateVideoPath,user_image,filename_prefix):
        image_face_fusion = ImageFaceFusion(model_dir=folder_paths.models_dir+'/image-face-fusion')
        restorer_model = GFPGANer(model_path=os.path.join(folder_paths.models_dir+'/upscale_models','GFPGANv1.4.pth'), upscale=1, arch='clean',
                                channel_multiplier=2, bg_upsampler=None)
        imageu_np=user_image.numpy()
        imau_shape=imageu_np.shape

        if imau_shape[0]<=0:
            return {"ui": {"text": "替换人脸照片不能为空"}, "result": ("",)}

        imageu=imageu_np[0]*255
        imageu=np.uint8(imageu)
        cap = cv2.VideoCapture(templateVideoPath)
        fps = cap.get(cv2.CAP_PROP_FPS)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        flag = cap.isOpened()
        if not flag:
            return {"ui": {"text": "视频打开失败"}, "result": ("",)}
        image_list=[]
        for frame_idx in tqdm(range(length), '融合进度:'):
        #while True:
            flag, frame_c = cap.read()
            if not flag:  # 如果已经读取到最后一帧则退出
                break
            frame = cv2.cvtColor(frame_c, cv2.COLOR_BGR2RGB) #bgr转rgb
            image=image_face_fusion.inference(frame_c,imageu)
            #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #bgr转rgb
            image_list.append(image)
            
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir, imau_shape[1], imau_shape[0])
        fileTemp = f"{filename}_{counter:05}_temp.mp4"
        videoPathTemp = os.path.join(full_output_folder, fileTemp)
        file = f"{filename}_{counter:05}_.mp4"
        videoPath = os.path.join(full_output_folder, file)
        with imageio.get_writer(videoPathTemp, fps=fps) as video:
            for i in tqdm(range(len(image_list)), '写入进度:'):
                image=image_list[i]
                _,_,rimage=restorer_model.enhance(image)
                if rimage is not None:
                    image=rimage
                video.append_data(image)# 写入视频
        fileAudio = f"{filename}_{counter:05}_temp.mp3"
        audioFilePathName=os.path.join(full_output_folder, fileAudio)
        aff = FFmpeg(inputs={templateVideoPath: None},outputs={audioFilePathName: '-f {} -vn'.format('mp3')})
        aff.run()
        _codec = 'copy'
        vff = FFmpeg(
            inputs={videoPathTemp: None, audioFilePathName: None},
            outputs={videoPath: '-map 0:v -map 1:a -c:v copy -c:a {} -shortest'.format(_codec)})
        vff.run()
        os.remove(videoPathTemp)
        os.remove(audioFilePathName)
        return {"ui": {"text": "视频保存成功文件地址："+videoPath,
        'videos':[{'filename':file,'type':'output','subfolder':'video'}]}, "result": (videoPath,)}

NODE_CLASS_MAPPINGS = {
    "VideoFaceFusion": VideoFaceFusion
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoFaceFusion": "视频脸部融合"
}
