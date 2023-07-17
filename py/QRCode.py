import qrcode
import numpy as np
import torch
class QRCode:
    """
    A example node

    Class methods
    -------------
    INPUT_TYPES (dict): 
        Tell the main program input parameters of nodes.

    Attributes
    ----------
    RETURN_TYPES (`tuple`): 
        The type of each element in the output tulple.
    RETURN_NAMES (`tuple`):
        Optional: The name of each output in the output tulple.
    FUNCTION (`str`):
        The name of the entry-point method. For example, if `FUNCTION = "execute"` then it will run Example().execute()
    OUTPUT_NODE ([`bool`]):
        If this node is an output node that outputs a result/image from the graph. The SaveImage node is an example.
        The backend iterates on these output nodes and tries to execute all their parents if their parent graph is properly connected.
        Assumed to be False if not present.
    CATEGORY (`str`):
        The category the node should appear in the UI.
    execute(s) -> tuple || None:
        The entry point method. The name of this method must be the same as the value of property `FUNCTION`.
        For example, if `FUNCTION = "execute"` then this method's name must be `execute`, if `FUNCTION = "foo"` then it must be `foo`.
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {"text": ("STRING",{"default": ""}),
                "version": ("INT", {"default": 1, "min": 1, "max": 40, "step": 1}),
                "box_size": ("INT", {"default": 10, "min": 1, "max": 500, "step": 10}),
                "border": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1}),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("二维码图片","遮罩层")

    FUNCTION = "QR_code"

    #OUTPUT_NODE = False

    CATEGORY = "lam"

    def QR_code(self, text,version,box_size,border):
        qr = qrcode.QRCode(
                version=version,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=box_size,
                border=border
                )#设置二维码的大小
        print(text)
        qr.add_data(text)  #这里是填网站
        qr.make(fit=True)
        img = qr.make_image()
        img = np.array(img)
        img2 = np.zeros((img.shape[0],img.shape[1],3))
        img2[:,:,0] = img
        img2[:,:,1] = img
        img2[:,:,2] = img
        mask = np.array(img).astype(np.float32) / 1.0
        mask = torch.from_numpy(mask)[None,]
        image = np.array(img2).astype(np.float32) / 1.0
        image = torch.from_numpy(image)[None,]
        print(mask.size(),image.size())
        return (image,mask)


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "QRCode": QRCode
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "QRCode": "二维码生成"
}
