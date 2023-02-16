# ⚡️ Lightning Research Poster Template 🔬

[![Lightning](https://img.shields.io/badge/-Lightning-792ee5?logo=pytorchlightning&logoColor=white)](https://lightning.ai)
![license](https://img.shields.io/badge/License-Apache%202.0-blue.svg)

Use this app to share your research paper results. This app lets you connect a blogpost, arxiv paper, and a jupyter
notebook and even have an interactive demo for people to play with the model. This app also allows industry
practitioners to reproduce your work.

## Getting started

To create a Research Poster you can install this app via the [Lightning CLI](https://lightning.ai/lightning-docs/) or
[use the template](https://docs.github.com/en/articles/creating-a-repository-from-a-template) from GitHub and
manually install the app as mentioned below.

### Installation

#### With Lightning CLI

`lightning install app lightning/research_poster`

#### Use GitHub template

Click on the "Use this template" button at the top, name your app repo, and GitHub will create a fork of this app to
your account.

> ![use-template.png](./assets/use-template.png)

You can clone the forked app repo and follow the steps below to install the app.

```
git clone https://github.com/YOUR-USERNAME/lightning-template-research-app.git
cd lightning-template-research-app
pip install -r requirements.txt
pip install -e .
```

Once you have installed the app, you can goto the `LAI-research-template-App` folder and
run `lightning run app app.py --cloud` from terminal.
This will launch the template app in your default browser with tabs containing research paper, blog, Training
logs, and Model Demo.

You should see something like this in your browser:

> ![image](./assets/demo.png)

### Steps to customize to your research

You can modify the content of this app and customize it to your research.
At the root of this template, you will find [app.py](./app.py) that contains the `ResearchApp` class. This class
provides arguments like a link to a paper, a blog, and whether to launch a Gradio demo. You can read more about what
each of the arguments does in the docstrings.

#### 1. Poster Component

This component lets you make research posters using markdown files. The component comes with a predefined poster.md file
in the resources folder that contains markdown content for building the poster. You can directly update the existing
file with your research content.

#### 2. Link to Paper, blog and Training Logs

You can add your research paper, a blog post, and training logs to your app. These are usually static web links that can
be directly passed as optional arguments within app.py

#### 3. A view only Jupyter Notebook

You can provide the path to your notebook and it will be converted into static HTML.

#### 4. Model Demo

To create an interactive demo you’d need to implement the `build_model` and `predict` methods of the ModelDemo class
present
in the `research_app/demo/model.py` module.

#### 5. JupyterLab Component

This component runs and adds a JupyterLab instance to your app. You can provide a way to edit and run your code for
quick audience demonstrations. However, note that sharing a JupyterLab instance can expose the cloud instance to
security vulnerability.

### Highlights

- Provide the link for paper, blog, or training logger like WandB as an argument, and `ResearchApp` will create a tab
  for each.
- Make a poster for your research by editing the markdown file in the [resources](./resources/poster.md) folder.
- Add interactive model demo with Gradio app, update the gradio component present in the \[research_app (
  ./research_app/demo/model.py) folder.
- View a Jupyter Notebook or launch a fully-fledged notebook instance (Sharing a Jupyter Notebook instance can expose
  the cloud instance to security vulnerability.)
- Reorder the tab layout using the `tab_order` argument.

### Example

```python
# update app.py at the root of the repo
import lightning as L

app = L.LightningApp(
    ResearchApp(
        poster_dir="resources",
        paper="https://arxiv.org/pdf/2103.00020.pdf",
        blog="https://openai.com/blog/clip/",
        training_log_url="https://wandb.ai/aniketmaurya/herbarium-2022/runs/2dvwrme5",
        github="https://github.com/mlfoundations/open_clip",
        notebook_path="resources/Interacting_with_CLIP.ipynb",
        launch_jupyter_lab=False,
        launch_gradio=True,
        tab_order=[
            "Poster",
            "Blog",
            "Paper",
            "Notebook",
            "Training Logs",
            "Model Demo",
        ],
    )
)
```

## FAQs

1. How to pull from the latest template
   code? [Answer](https://stackoverflow.com/questions/56577184/github-pull-changes-from-a-template-repository)
