import requests
import re
class YouDaoTranslate:
    """
    中文翻译有道免费接口调用
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        """
            Return a dictionary which contains config for all input fields.
            Some types (string): "MODEL", "VAE", "CLIP", "CONDITIONING", "LATENT", "IMAGE", "INT", "STRING", "FLOAT".
            Input types "INT", "STRING" or "FLOAT" are special values for fields on the node.
            The type can be a list for selection.

            Returns: `dict`:
                - Key input_fields_group (`string`): Can be either required, hidden or optional. A node class must have property `required`
                - Value input_fields (`dict`): Contains input fields config:
                    * Key field_name (`string`): Name of a entry-point method's argument
                    * Value field_config (`tuple`):
                        + First value is a string indicate the type of field or a list for selection.
                        + Secound value is a config for type "INT", "STRING" or "FLOAT".
        """
        return {
            "required": {
                "type": (["ZH_CN2EN","EN2ZH_CN"], ),
                "text": ("STRING", {"multiline": True})
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("译文",)

    FUNCTION = "translate"

    #OUTPUT_NODE = False

    CATEGORY = "lam"

    def translate(self, text,type):
        resText=text
        if text and ((type=='ZH_CN2EN' and is_contains_chinese(text)) or (type=='EN2ZH_CN' and is_contains_english(text))) :
            data = { 'doctype': 'json', 'type': type,'i': text}
            r = requests.get("http://fanyi.youdao.com/translate",params=data)
            result = r.json()
            print(result)
            resText=result['translateResult'][0][0]['tgt']
        return (resText,)

def is_contains_chinese(strs): #判断是否包含中文
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False

def is_contains_english(str): #判断是否包含英文
    my_re = re.compile(r'[A-Za-z]', re.S)
    res = re.findall(my_re, str)
    if len(res):
        return True
    else:
        return False

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "YouDaoTranslate": YouDaoTranslate
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "YouDaoTranslate": "有道翻译"
}
