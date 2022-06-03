import enum
import logging
import os.path
import urllib
from typing import List

import gradio as gr
import numpy as np
import pandas as pd
from lightning.components.serve import ServeGradio
from rich import print
from transformers import CLIPModel, CLIPProcessor

logger = logging.getLogger(__name__)


def download_files():
    print("Downloading embeddings, this might take some time!")
    urllib.request.urlretrieve(
        "https://github.com/aniketmaurya/temp-poster-assets/blob/main/embeddings.npy?raw=true",
        "resources/embeddings.npy",
    )
    urllib.request.urlretrieve(
        "https://github.com/aniketmaurya/temp-poster-assets/blob/main/embeddings2.npy?raw=true",
        "resources/embeddings2.npy",
    )
    urllib.request.urlretrieve(
        "https://github.com/aniketmaurya/temp-poster-assets/blob/main/data.csv?raw=true",
        "resources/data.csv",
    )
    urllib.request.urlretrieve(
        "https://drive.google.com/uc?export=download&id=19aVnFBY-Rc0-3VErF_C7PojmWpBsb5wk",
        "resources/data2.csv",
    )
    print("✅ Downloaded embeddings")


if not os.path.exists("resources/data.csv"):
    download_files()

df = {0: pd.read_csv("resources/data.csv"), 1: pd.read_csv("resources/data2.csv")}
EMBEDDINGS = {
    0: np.load("resources/embeddings.npy"),
    1: np.load("resources/embeddings2.npy"),
}
for k in [0, 1]:
    EMBEDDINGS[k] = np.divide(EMBEDDINGS[k], np.sqrt(np.sum(EMBEDDINGS[k] ** 2, axis=1, keepdims=True)))
source = {0: "\nSource: Unsplash", 1: "\nSource: The Movie Database (TMDB)"}


def get_html(url_list, height=200):
    html = "<div style='margin-top: 20px; display: flex; flex-wrap: wrap; justify-content: space-evenly'>"
    for url, title, link in url_list:
        html2 = f"<img title='{title}' style='height: {height}px; margin-bottom: 10px' src='{url}'>"
        if len(link) > 0:
            html2 = f"<a href='{link}' target='_blank'>" + html2 + "</a>"
        html = html + html2
    html += "</div>"
    return html


class DATASET(enum.Enum):
    UNSPLASH = "Unsplash"
    MOVIES = "Movies"


dataset = DATASET.MOVIES.value


class CLIP:
    def __init__(self, processor, model):
        self.processor = processor
        self.model = model

    def compute_text_embeddings(self, list_of_strings: List[str]):
        inputs = self.processor(text=list_of_strings, return_tensors="pt", padding=True)
        return self.model.get_text_features(**inputs)

    def image_search(self, query: str, n_results=24):
        assert isinstance(query, str), f"query is of type {type(query)}"
        text_embeddings = self.compute_text_embeddings([query]).detach().numpy()
        k = 0 if dataset == "Unsplash" else 1
        results = np.argsort((EMBEDDINGS[k] @ text_embeddings.T)[:, 0])[-1 : -n_results - 1 : -1]  # noqa E203
        result = [(df[k].iloc[i]["path"], df[k].iloc[i]["tooltip"] + source[k], df[k].iloc[i]["link"]) for i in results]
        return result


def predict(model, query: str) -> str:
    results = model.image_search(query)
    return get_html(results)


class ModelDemo(ServeGradio):
    """Serve model with Gradio UI.

    You need to define i. `build_model` and ii. `predict` method and Lightning `ServeGradio` component will
    automatically launch the Gradio interface.
    """

    inputs = gr.inputs.Textbox(default="Doctor Strange Multiverse", label="Search your favourite movie here")
    outputs = gr.outputs.HTML(label="Fetch Images from <b>themoviedb.org</b>")

    def __init__(
        self,
    ):
        super(ServeGradio, self).__init__(parallel=True)
        self._model = None
        self.ready = False
        print("initializing Model Demo...")

    def build_model(self):
        print("loading model...")
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").eval()
        for p in model.parameters():
            p.requires_grad = False
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        clip = CLIP(processor=processor, model=model)
        print("built model!")
        self.ready = True
        return clip

    def predict(self, query: str):
        results = self.model.image_search(query)
        return get_html(results)


if __name__ == "__main__":
    demo = ModelDemo()
    demo.run()
