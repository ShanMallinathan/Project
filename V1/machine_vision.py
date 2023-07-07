#Function to load and evaluate machine learning model

import torch
import torchvision.models as models
from torchvision.io.image import read_image
from PIL import Image
from torchvision.transforms.functional import pil_to_tensor

#Class to encapsulate models and its associated functions
class model:
    def __init__(self, select_model = models.detection.fasterrcnn_mobilenet_v3_large_320_fpn(weights='DEFAULT')):
        self.select_model = select_model
        print("Evaluating the model")
        select_model.eval()
        print("Model has been evaluated successfully")
    
    def return_model(self):
        return self.select_model
    
    def objdet_init(self, input_feed, required_label=1):
        #Convert the frame into PIL image
        image = Image.fromarray(input_feed)
        preprocess = pil_to_tensor(image)
        preprocess = preprocess.unsqueeze(dim=0)
        input_image = preprocess/255.0
        predictions = self.select_model(input_image)
        max_score = -1
        min_box = None
        #get the max confidence of the required label
        if(len(predictions[0]['boxes'])>=1):
            for i in range(len(predictions)):
                if predictions[i]['labels'][0].item() == required_label:
                    if predictions[i]['scores'][0].item()>max_score:
                        min_box = predictions[i]['boxes'][0].tolist()
        x = None
        y = None
        x1 =  None
        y1 = None
        x2 = None
        y2 = None
        if min_box is not None:
            x1 = int(min_box[0])
            y1 = int(min_box[1])
            x2 = int(min_box[2])
            y2 = int(min_box[3])
            x = int(x1 + (x2-x1)/2)
            y = int(y1 + (y2-y1)/2)
            return 1, x, y, x1, y1, x2, y2
        else:
            return 0,-1,-1,-1,-1,-1,-1