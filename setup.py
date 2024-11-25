from setuptools import setup, find_packages

setup(
    name="viscli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "matplotlib",
        "faiss-cpu",
        "openai"
    ],
    entry_points={
        'console_scripts': [
            'viscli = viscli.cli:main',
        ],
    },
)
