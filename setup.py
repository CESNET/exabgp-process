from setuptools import setup, find_packages

setup(
    name="exabgp_process",
    version="1.0.0",
    description="Process for ExaBGP, started by ExaBGP service",
    author="Jiri Vrany",
    author_email="jiri.vrany@cesnet.cz",
    packages=find_packages(),
    install_requires=["pika", "python-dotenv", "loguru", "click", "flask"],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "exabgp-process=exabgp_process:main",
        ],
    },
)
