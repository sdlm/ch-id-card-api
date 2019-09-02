import torch
from PIL import Image
from torch import nn
from torchvision import models
from torchvision.transforms import transforms

MODEL_PATH = "/weights/resnet18_classification_v1.1.2.pt"


def load_model(weights_path: str = None):
    model = models.resnet18()
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, 2)

    path = weights_path if weights_path else MODEL_PATH
    model.load_state_dict(torch.load(path, map_location="cpu"))
    model.eval()

    return model


def predict_existence(model, tensor) -> bool:
    predicted_labels = model(tensor)
    return predicted_labels[0][0].item() < predicted_labels[0][1].item()


def get_card_existence(img: Image) -> bool:
    model = load_model()
    tensor = transforms.ToTensor()(img).unsqueeze(0)
    return predict_existence(model, tensor)
