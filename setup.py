from setuptools import find_packages, setup

setup(
    name="streamlit-poll",
    version='22.8.17',
    packages=find_packages(exclude=("tests", "docs")),
    description="Simple app to run a poll/quiz using streamlit",
    url="URL",
    author="Srinivas Gorur-Shandilya",
    author_email="code@srinivas.gs",
    install_requires=["streamlit", "pandas"],
)
