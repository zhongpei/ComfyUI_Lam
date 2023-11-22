import insightface
import numpy as np
import cv2
import threading
from typing import Any, Optional, List

providers = ["CPUExecutionProvider"]
THREAD_LOCK = threading.Lock()
FACE_ANALYSER = None

def getFaceSwapModel(model_path: str):
    
    FS_MODEL = insightface.model_zoo.get_model(model_path, providers=providers)
    return FS_MODEL

def get_face_analyser() -> Any:
    global FACE_ANALYSER

    with THREAD_LOCK:
        if FACE_ANALYSER is None:
            FACE_ANALYSER = insightface.app.FaceAnalysis(name='buffalo_l', providers=providers)
    return FACE_ANALYSER

def getFaceAnalyser():
    face_analyser=insightface.app.FaceAnalysis(name="buffalo_l", providers=providers)
    return face_analyser

def get_face_single(img_data: np.ndarray,face_index=0, det_size=(640, 640)):
    face_analyser = get_face_analyser()
    face_analyser.prepare(ctx_id=0, det_size=det_size)
    face = face_analyser.get(img_data)

    if len(face) == 0 and det_size[0] > 320 and det_size[1] > 320:
        det_size_half = (det_size[0] // 2, det_size[1] // 2)
        return get_face_single(img_data, face_index=face_index, det_size=det_size_half)

    try:
        return sorted(face, key=lambda x: x.bbox[0])[face_index]
    except IndexError:
        return None



