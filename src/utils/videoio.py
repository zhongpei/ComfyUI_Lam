import shutil
import uuid
import folder_paths
import os

import cv2

def load_video_to_cv2(input_path):
    video_stream = cv2.VideoCapture(input_path)
    fps = video_stream.get(cv2.CAP_PROP_FPS)
    full_frames = [] 
    while 1:
        still_reading, frame = video_stream.read()
        if not still_reading:
            video_stream.release()
            break 
        full_frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    return full_frames

def save_video_with_watermark(video, audio, save_path, watermark=False):
    temp_file = str(uuid.uuid4())+'.mp4'
    cmd = r'ffmpeg -y -hide_banner -loglevel error -i "%s" -i "%s" -vcodec copy "%s"' % (video, audio, temp_file)
    os.system(cmd)

    if watermark is False:
        shutil.move(temp_file, save_path)
    else:
        dir_path = folder_paths.get_annotated_filepath('custom_nodes')
        watarmark_path = dir_path+"/ComfyUI_Lam/docs/sadtalker_logo.png"

        cmd = r'ffmpeg -y -hide_banner -loglevel error -i "%s" -i "%s" -filter_complex "[1]scale=100:-1[wm];[0][wm]overlay=(main_w-overlay_w)-10:10" "%s"' % (temp_file, watarmark_path, save_path)
        os.system(cmd)
        os.remove(temp_file)