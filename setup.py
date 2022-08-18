"""install this using pip install -e ."""

from setuptools import find_packages, setup

setup(
    name="streamlit-poll",
    version='22.8.18',
    packages=find_packages(exclude=("tests", "docs")),
    description="Simple app to run a poll/quiz using streamlit",
    url="https://github.com/sg-s/streamlit-poll",
    author="Srinivas Gorur-Shandilya",
    author_email="code@srinivas.gs",
    install_requires=["streamlit", "pandas"],
)
