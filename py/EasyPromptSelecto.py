import server
from aiohttp import web
import os
import yaml


dir = os.path.abspath(os.path.join(__file__, "../../tags"))
if not os.path.exists(dir):
    os.mkdir(dir)

@server.PromptServer.instance.routes.get("/lam/getPrompt")
def getPrompt(request):
    if "name" in request.rel_url.query:
        name = request.rel_url.query["name"]
        file = os.path.join(dir, name+'.yml')
        if os.path.isfile(file):
            f = open(file,'r', encoding='utf-8')
            data = yaml.load(f, Loader=yaml.FullLoader)
            f.close()
            #转json
            if data:
                return web.json_response(data)
    return web.Response(status=404)

class EasyPromptSelecto:
    """
    提示词选择工具
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        dir = os.path.abspath(os.path.join(__file__, "../../tags"))
        if not os.path.exists(dir):
            os.mkdir(dir)
        #获取目录全部yml文件名
        files_name=[]
        for root, dirs, files in os.walk(dir):
            for file in files:
                if file.endswith(".yml"):
                    files_name.append(file.split(".")[0])

        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "prompt_type":(files_name, ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("提示词",)

    FUNCTION = "translate"

    #OUTPUT_NODE = False

    CATEGORY = "lam"

    def translate(self,text,**args):
        return (text,)

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "EasyPromptSelecto": EasyPromptSelecto
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "EasyPromptSelecto": "提示词选择工具"
}
