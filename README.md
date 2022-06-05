# Lightning Research Poster Template

Use this app to share your research paper results. This app lets you connect a blogpost, arxiv paper, and a jupyter
notebook and even have an interactive demo for people to play with the model. This app also allows industry
practitioners to reproduce your work.

## Getting started

Use this template and customize for your research paper.

### Installation

#### With Lightning

`lightning install app lightning/research_poster`

#### Manual

```
git clone https://github.com/PyTorchLightning/lightning-template-research-app.git
cd lightning-template-research-app
pip install -r requirements.txt
pip install -e .
```

Once you have installed the app, you can goto the `lightning-template-research-app` folder and
run `lightning run app app.py` from terminal.
This will launch the template app in your default browser with multiple tabs containing research paper, blog, Training
logs, and Model Demo.
To share your research, you should modify the content of this app.

At the root of this template you will find [app.py](./app.py) that contains `ResearchApp` class, this class provides
arguments like link to paper, blog, and whether to launch a Gradio demo. You can read more about what each of the
arguments do in the docstrings.

#### Highlights

- Provide the link for paper, blog or training log manager like WandB as argument and `ResearchApp` will
  create a tab for each of these.
- Make a poster for your research by editing the markdown file in the [resources](./resources/poster.md) folder.
- Add interactive model demo with Gradio app, update the gradio component present in
  the [research_app](./research_app/components/model_demo.py) folder.
- Launch Jupyter Notebook to show the code demo.

```python
# update app.py at the root of the repo
import lightning as L

paper = "https://arxiv.org/pdf/2103.00020.pdf"
blog = "https://openai.com/blog/clip/"
github = "https://github.com/mlfoundations/open_clip"
wandb = "https://wandb.ai/aniketmaurya/herbarium-2022/runs/2dvwrme5"
tabs = ["Poster", "Blog", "Paper", "Notebook", "Training Logs", "Model Demo"]

app = L.LightningApp(
    ResearchApp(
        resource_path="resources",
        paper=paper,
        blog=blog,
        training_log_url=wandb,
        github=github,
        notebook_path="resources/Interacting_with_CLIP.ipynb",
        launch_jupyter_lab=True,
        launch_gradio=True,
        tab_order=tabs,
    )
)
```

To run this app, launch the terminal and run `lightning run app app.py`

You should see something like this in your browser:

![image](./assets/demo.png)
