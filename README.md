# lightning-template-research-app

## Get started
```bash
git clone https://github.com/PyTorchLightning/lightning.git
cd lightning
mamba create --name paper_app python=3.10 -y
conda activate paper_app
pip install -r requirements.txt  # mandatory step to pull the dependencies from extra-index-url
pip install -e .
python scripts/download_frontend.py
# research-app
cd ..
git clone https://github.com/PyTorchLightning/lightning-template-research-app.git
cd lightning-template-research-app
pip install -e ".[dev]"
```

### local run
```bash
lightning build app research_app/app.py --name jupyter-`date -u +%H:%M`
```
