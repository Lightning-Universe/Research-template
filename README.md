# lightning-template-research-app

## Get started

```bash
git clone https://github.com/PyTorchLightning/lightning.git
cd lightning
mamba create --name paper_app python=3.10 -y
conda activate paper_app
# mandatory step to pull the dependencies from extra-index-url
pip install -r requirements.txt
pip install -e .
python scripts/download_frontend.py
# research-app
cd ..
git clone https://github.com/PyTorchLightning/lightning-template-research-app.git
cd lightning-template-research-app
python setup.py install develop
```

### local run

```bash
lightning run app app.py --name poster-`date -u +%H:%M`
```

### Making contributions

Submit a pull request to the `lightning-template-research-app` repository.
Run pre-commit locally to check for any errors before committing: `pre-commit run --all-files`.
