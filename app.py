from lightning import LightningApp

from research_app import ResearchApp

if __name__ == "__main__":
    resource_path = "resources"
    paper = "https://arxiv.org/pdf/2103.00020"
    blog = "https://openai.com/blog/clip/"
    github = "https://github.com/openai/CLIP"
    wandb = "https://wandb.ai/dalle-mini/dalle-mini/runs/3r9ew7qt?workspace="

    app = LightningApp(
        ResearchApp(
            resource_path=resource_path,
            paper=paper,
            blog=blog,
            experiment_manager=wandb,
            enable_notebook=True,
            enable_gradio=True,
        )
    )
