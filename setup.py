from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="complexity-tracker",
    version="0.1.0",
    author="DataGriff",
    description="A complexity tracker for analyzing code complexity across repositories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyYAML>=6.0.1",
        "GitPython>=3.1.40",
        "radon>=6.0.1",
        "matplotlib>=3.8.2",
        "plotly>=5.18.0",
        "Jinja2>=3.1.3",
        "requests>=2.31.0",
        "pygments>=2.17.2",
        "pandas>=2.1.4",
        "lizard>=1.17.10",
    ],
    entry_points={
        "console_scripts": [
            "complexity-tracker=complexity_tracker.cli:main",
        ],
    },
)
