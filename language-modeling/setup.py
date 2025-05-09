from setuptools import setup, find_packages

setup(
    name="reasoning-in-chains",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "torch",
        "transformers",
        "pgmpy",
        "networkx",
        "pandas",
        "pyprojroot",
    ],
)