import torch
import torchvision.models as models
import cv2
from torchvision.io.image import read_image
from PIL import Image
from torchvision.transforms.functional import pil_to_tensor

#defining mobinet v3 model
model = models.detection.fasterrcnn_resnet50_fpn(weights=True)
model_lite = models.detection.fasterrcnn_mobilenet_v3_large_320_fpn(weights=True)
model2 = models.detection.ssdlite320_mobilenet_v3_large(pretrained=True)
model_shuffle = models.shufflenet_v2_x0_5(pretrained=True)

#evaluating the model
model.eval()
model_lite.eval()
model2.eval()
model_shuffle.eval()

#Predictions
image = Image.open('/home/shanthinath/project/mustang.jpg')
preprocess = pil_to_tensor(image)
preprocess = preprocess.unsqueeze(dim=0)
input_image = preprocess/255.0
predictions = model(input_image)
print(predictions[0][0])