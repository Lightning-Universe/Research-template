import setuptools

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="research_app",
    version="0.0.1",
    description="Research App",
    author="Grid.ai",
    packages=setuptools.find_packages(where="research_app*"),
    install_requires=[requirements],
    include_package_data=True,
    extras_require={
        "dev": ["ipdb==0.13.9", "black==22.3.0", "isort==5.10.1"],
    },
    python_requires=">=3.8",
)
