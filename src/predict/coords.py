import numpy as np
import torch
from PIL import Image
from torch import nn
from torchvision import models
from torchvision.transforms import transforms

MODEL_PATH = "/weights/resnet50_regression_v2.2.3.pt"


def load_model(weights_path: str = None):
    model = models.resnet50()
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, 8)

    path = weights_path if weights_path else MODEL_PATH
    model.load_state_dict(torch.load(path))
    model.eval()

    return model


def predict_coords(model, tensor):
    coords = model(tensor)
    coords = torch.split(coords, 1, dim=1)
    coords = np.resize(coords, (4, 2))
    return coords


def get_card_coords(img: Image) -> np.array:
    model = load_model()
    tensor = transforms.ToTensor()(img).unsqueeze(0)
    return predict_coords(model, tensor)
