from setuptools import setup, find_packages

setup(
    name="ExaBGP API",
    version="0.1.0",
    description="API for ExaBGP, started by ExaBGP process",
    author="Jiri Vrany",
    author_email="jiri.vrany@cesnet.cz",
    packages=find_packages(),
    install_requires=[
        "pika",
        "python-dotenv",
        "loguru",
        "click",
        "flask"
    ],
    python_requires='>=3.7',
    entry_points={
        "console_scripts": [
            "exabgp-api=exabgp_api:main",
        ],
    },
)
