import importlib.util
import glob
import os
import sys
from .lam import init, get_ext_dir

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

if init():
    py = get_ext_dir("py")
    #用os取目录下所有py文件
    #files = glob.glob(os.path.join(py, "*.py"), recursive=False)
    files = os.listdir(py)
    for file in files:
        if not file.endswith(".py"):
            continue
        #取文件名
        name = os.path.splitext(file)[0]
        imported_module = importlib.import_module(".py.{}".format(name), __name__)
        NODE_CLASS_MAPPINGS = {**NODE_CLASS_MAPPINGS, **imported_module.NODE_CLASS_MAPPINGS}
        NODE_DISPLAY_NAME_MAPPINGS = {**NODE_DISPLAY_NAME_MAPPINGS, **imported_module.NODE_DISPLAY_NAME_MAPPINGS}
        # spec = importlib.util.spec_from_file_location(name, file)
        # module = importlib.util.module_from_spec(spec)
        # sys.modules[name] = module
        # spec.loader.exec_module(module)
        # if hasattr(module, "NODE_CLASS_MAPPINGS") and getattr(module, "NODE_CLASS_MAPPINGS") is not None:
        #     NODE_CLASS_MAPPINGS.update(module.NODE_CLASS_MAPPINGS)
        #     if hasattr(module, "NODE_DISPLAY_NAME_MAPPINGS") and getattr(module, "NODE_DISPLAY_NAME_MAPPINGS") is not None:
        #         NODE_DISPLAY_NAME_MAPPINGS.update(module.NODE_DISPLAY_NAME_MAPPINGS)

#WEB_DIRECTORY = "./js"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
