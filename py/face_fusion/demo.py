from image_face_fusion import ImageFaceFusion
import numpy as np
from numpy import ndarray
from PIL import Image
import cv2 
image_face_fusion = ImageFaceFusion(model_dir='C:/Users/Administrator/.cache/modelscope/hub/damo/cv_unet-image-face-fusion_damo')

template_path = 'F:/SadTalker/examples/source_image/full_body_1.png'
user_path = 'F:/ComfyUI/input/mbg.png'
#template=Image.open(template_path)
#template=Image.fromarray(np.uint8(template))

rimg=image_face_fusion.inference(template_path,user_path)
cv2.imwrite('F:/FaceFusion/result8.png', rimg)
print('finished!')

