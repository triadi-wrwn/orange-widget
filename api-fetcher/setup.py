from setuptools import setup

setup(
    name="Demo",
    packages=["ApiFetcherWidget"],
    package_data={"ApiFetcherWidget": ["icons/*.svg"]},
    classifiers=["Example :: Invalid"],
    # Declare orangedemo package to contain widgets for the "Demo" category
    entry_points={"orange.widgets": "Demo = ApiFetcherWidget"},
)