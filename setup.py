import subprocess

import setuptools
from setuptools.command.install import install


class PostBuild(install):
    """Run _post_install function after install is complete."""

    def run(self):
        install.run(self)
        self.execute(
            _post_install, (self.install_lib,), msg="Running post install task"
        )


def _post_install(dir):
    cmd = "/bin/bash bash_scripts/build_mkposters.sh"
    with subprocess.Popen(
        cmd.split(" "),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=0,
        close_fds=True,
    ) as proc:
        if proc.stdout:
            with proc.stdout:
                for line in iter(proc.stdout.readline, b""):
                    print(line.decode().rstrip())
        exit_code = proc.wait()
        if exit_code != 0:
            raise Exception(exit_code)


with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="research_app",
    version="0.0.1",
    description="Research App",
    author="Grid.ai",
    packages=setuptools.find_packages(where="research_app*"),
    install_requires=[requirements],
    include_package_data=False,
    extras_require={
        "dev": [
            "ipdb==0.13.9",
            "black==22.3.0",
            "isort==5.10.1",
            "pre-commit==2.18.1",
        ],  # E501
    },
    cmdclass={"install": PostBuild},
    python_requires=">=3.8",
)
