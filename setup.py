from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mising",
    version="0.1.0",
    author="Mising NLP Project Contributors",
    description="Natural Language Processing library for the Mising language of Assam",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mising-nlp/mising",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.7",
    install_requires=[],
    extras_require={
        "dev": ["pytest>=7.0", "flake8>=5.0"],
    },
    entry_points={
        "console_scripts": [
            "mising=mising.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "mising": ["data/*.json", "data/*.txt"],
    },
)
