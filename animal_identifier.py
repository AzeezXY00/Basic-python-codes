import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import urllib.request
import json
import sys
import os

# Download ImageNet class labels
LABELS_URL = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
LABELS_FILE = "imagenet_labels.json"

if not os.path.exists(LABELS_FILE):
    print("Downloading ImageNet labels...")
    urllib.request.urlretrieve(LABELS_URL, LABELS_FILE)

with open(LABELS_FILE) as f:
    labels = json.load(f)

# Load pretrained ResNet18
print("Loading pretrained ResNet18...")
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
model.eval()

# Preprocessing — must match what ResNet was trained with
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# Load and classify image
image_path = sys.argv[1] if len(sys.argv) > 1 else "cat.jpeg"
print(f"Classifying: {image_path}\n")

image = Image.open(image_path).convert("RGB")
tensor = transform(image).unsqueeze(0)

with torch.no_grad():
    output = model(tensor)
    probabilities = torch.nn.functional.softmax(output[0], dim=0)

# Top 5 results
top5 = torch.topk(probabilities, 5)
print("Top 5 Predictions:")
print("-" * 40)
for prob, idx in zip(top5.values, top5.indices):
    bar = "█" * int(prob.item() * 30)
    print(f"  {labels[idx.item()]:<25} {prob.item()*100:5.2f}% {bar}")