# lightning-template-research-app

Research Poster App helps Authors and Readers to publish and view research, code, experiment reports,
articles or any resource within the same app.

## Get started

You can fork or clone this template app and start editing or overriding the content.

### Installation

Step 1: Install `lightning`

```bash
git clone https://github.com/PyTorchLightning/lightning.git
cd lightning
# mandatory step to pull the dependencies from extra-index-url
pip install -r requirements.txt
pip install -e .
python scripts/download_frontend.py
```

Step 2: Clone Research App

```
git clone https://github.com/PyTorchLightning/lightning-template-research-app.git
cd lightning-template-research-app
python setup.py install develop
```

### How to Run?

**1. Run locally**
`` lightning run app app.py --name poster-`date -u +%H:%M ``

**2. Run on the Lightning cloud**
`` lightning run app app.py --name poster-`date -u +%H:%M --cloud ``

### Making contributions

**Step 1:** Install the `pre-commit` hook `pre-commit install`.

**Step 2:** Create a new branch with your code changes.

(Optional) Run pre-commit locally to check for any errors before committing: `pre-commit run --all-files`.

**Step 3:** Submit a pull request to the `lightning-template-research-app` main branch repository.
