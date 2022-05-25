from lightning import LightningApp

from research_app import ResearchApp

if __name__ == "__main__":
    resource_path = "resources"
    paper = "https://arxiv.org/pdf/2102.12092"
    blog = "https://wandb.ai/dalle-mini/dalle-mini/reports/DALL-E-Mini-Explained-with-Demo--Vmlldzo4NjIxODA"
    github = "https://github.com/borisdayma/dalle-mini"
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
