import logging

import gradio as gr
import numpy as np
import torch
from flash.image import ImageClassifier
from PIL import Image

logger = logging.getLogger(__name__)

model = ImageClassifier.load_from_checkpoint("image_classification_model.pt").eval()

IMAGE_SIZE = 224, 224
LABELS = ["ants", "bees"]


def predict(image: np.ndarray) -> str:
    image = Image.fromarray(image)
    image = image.resize(IMAGE_SIZE)
    image = np.asarray(image).astype(np.float32)
    image = image / 255.0
    image = np.expand_dims(image, 0)
    x = torch.as_tensor(image)
    x = x.permute(0, 3, 1, 2)
    label_idx = model(x).softmax(1).argmax()
    return LABELS[label_idx.tolist()]


iface = gr.Interface(
    fn=predict,
    inputs="image",
    outputs="text",
)

if __name__ == "__main__":
    iface.launch()
