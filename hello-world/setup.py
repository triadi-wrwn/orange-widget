from setuptools import setup

setup(
    name="Kategori Baru",
    packages=["helloworld"],
    package_data={"helloworld": ["icons/*.svg"]},
    classifiers=["Example :: Invalid"],
    # Declare orangedemo package to contain widgets for the "Demo" category
    entry_points={"orange.widgets": "Kategori Baru = helloworld"},
)