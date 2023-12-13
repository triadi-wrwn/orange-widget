from setuptools import setup

setup(
    name="Demo",
    packages=["demo-word"],
    package_data={"demo-word": ["icons/*.svg"]},
    classifiers=["Example :: Invalid"],
    # Declare orangedemo package to contain widgets for the "Demo" category
    entry_points={"orange.widgets": "Demo = demoword"},
)