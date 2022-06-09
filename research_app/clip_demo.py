"""This module implements the demo for CLIP model.

This demo is inspired from the work of [Vivien](https://github.com/vivien000).
Checkout the original implementation [here]((https://github.com/vivien000/clip-demo)

The app integration is done at `research_app/components/model_demo.py`.
"""
import enum
import logging
import os.path
import urllib
from typing import List

import numpy as np
import pandas as pd
from rich import print
from rich.logging import RichHandler
from transformers import CLIPModel, CLIPProcessor

FORMAT = "%(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])

logger = logging.getLogger(__name__)


class DATASET(enum.Enum):
    UNSPLASH = "Unsplash"
    MOVIES = "Movies"


dataset = DATASET.UNSPLASH.value


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
    logger.info("✅ Downloaded embeddings")


def get_html(url_list, height=200):
    html = "<div style='margin-top: 20px; display: flex; flex-wrap: wrap; justify-content: space-evenly'>"
    for url, title, link in url_list:
        html2 = f"<img title='{title}' style='height: {height}px; margin-bottom: 10px' src='{url}'>"
        if len(link) > 0:
            html2 = f"<a href='{link}' target='_blank'>" + html2 + "</a>"
        html = html + html2
    html += "</div>"
    return html


class CLIPDemo:
    def _pre_setup(self):
        if not os.path.exists("resources/data.csv"):
            download_files()

        self.df = {0: pd.read_csv("resources/data.csv"), 1: pd.read_csv("resources/data2.csv")}
        self.EMBEDDINGS = {
            0: np.load("resources/embeddings.npy"),
            1: np.load("resources/embeddings2.npy"),
        }
        for k in [0, 1]:
            self.EMBEDDINGS[k] = np.divide(
                self.EMBEDDINGS[k], np.sqrt(np.sum(self.EMBEDDINGS[k] ** 2, axis=1, keepdims=True))
            )
        self.source = {0: "\nSource: Unsplash", 1: "\nSource: The Movie Database (TMDB)"}

    def __init__(self):
        self.source = None
        self.df = None
        self.EMBEDDINGS = None

        self._pre_setup()

        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").eval()
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        for p in self.model.parameters():
            p.requires_grad = False

    def _compute_text_embeddings(self, list_of_strings: List[str]):
        inputs = self.processor(text=list_of_strings, return_tensors="pt", padding=True)
        return self.model.get_text_features(**inputs)

    def _image_search(self, query: str, n_results=24):
        assert isinstance(query, str), f"query is of type {type(query)}"
        text_embeddings = self._compute_text_embeddings([query]).detach().numpy()
        k = 0 if dataset == "Unsplash" else 1
        results = np.argsort((self.EMBEDDINGS[k] @ text_embeddings.T)[:, 0])[-1 : -n_results - 1 : -1]  # noqa E203
        result = [
            (self.df[k].iloc[i]["path"], self.df[k].iloc[i]["tooltip"] + self.source[k], self.df[k].iloc[i]["link"])
            for i in results
        ]
        return result

    def predict(self, query: str) -> str:
        results = self._image_search(query)
        return get_html(results)
