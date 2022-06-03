# Lightning Research Poster Template

Use this app to share your research paper results. This app lets you connect a blogpost, arxiv paper, and a
notebook and even have an interactive demo for people to play with the model. This app also allows industry
practitioners to reproduce your work.

@Aniket this is repetitive
Research Poster App helps Authors and Readers to publish and view research, code, experiment reports,
articles or any resource within the same app.

## Getting started

@Aniket explain how to use the template (ie. do I use the github greenbutton?)
Use this template and customize for your research paper.

### Installation

#### With Lightning

`lightning install app lightning/research_poster`
@Aniket you might want to add the command to run it as well once you installed it.

#### Manual

```
git clone https://github.com/PyTorchLightning/lightning-template-research-app.git
cd lightning-template-research-app
pip install -r requirements.txt
pip install -e .
```

### Share Research with Lightning App

The poster app has a `ResearchApp` class that provides flags that you can use to quickly build an app without knowing
any web development.
@Aniket is this true? What about the gradio side. Is this web development?

#### Highlights

- Provide the link for paper, blog or training log manager like WandB as argument and `ResearchApp` will
  create a tab for each of these.
  @Aniket what is optional / mandatory?
- Make a poster for your research by editing the markdown file in the [resources](./resources/poster.md) folder.
- Add interactive model demo with Gradio app, update the gradio component present in
  the [research_app](./research_app/components/model_demo.py) folder.
- Launch Jupyter Notebook to show the code demo.
  @Aniket is this relevant the jupyter side now?

```python
# update app.py at the root of the repo
import lightning as L

paper = "https://arxiv.org/pdf/2103.00020.pdf"
blog = "https://openai.com/blog/clip/"
github = "https://github.com/mlfoundations/open_clip"
wandb = "https://wandb.ai/aniketmaurya/herbarium-2022/runs/2dvwrme5"
# @Aniket why do you need to specify the tabs?
tabs = ["Poster", "Blog", "Paper", "Notebook", "Training Logs", "Model Demo"]
# @Aniket how is gradio being working here? What if my app need image upload, how do I do it?
app = L.LightningApp(
    ResearchApp(
        resource_path="resources",
        paper=paper,
        blog=blog,
        training_log_url=wandb,
        github=github,
        notebook_path="resources/Interacting_with_CLIP.ipynb",
        launch_jupyter_lab=True,  # TODO: Add comment what does it do
        launch_gradio=True,  # TODO: Add comment what does it do
        tab_order=tabs,
    )
)
```

To run this app, launch the terminal and run `lightning run app app.py`
@Aniket maybe use --cloud by default :)

You should see something like this in your browser:

![image](./assets/demo.png)
