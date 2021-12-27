"""
    AnonymousPlatform
    ~~~~~~


"""
import ast
import re
import os
from setuptools import setup, find_packages


def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, *parts), "r") as fp:
        return fp.read()


long_description = read("README.md")


setup(
    name="flaskbb-plugin-AnonymousPlatform",
    version="0.1.0",
    url="https://github.com/yihangalan/yihangalan-flaskbb-plugin-AnonymousPlatform",
    author="Fengyuan Ran",
    license="BSD",
    author_email="1337386019@qq.com",
    description="A AnonymousPlatform plugin for FlaskBB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="flaskbb plugin AnonymousPlatform",
    packages=find_packages("."),
    include_package_data=False,
    # package_data={
    #     "": ["AnonymousPlatform/translations/*/*/*.mo", "AnonymousPlatform/translations/*/*/*.po"]
    # },
    zip_safe=False,
    platforms="any",
    entry_points={"flaskbb_plugins": ["AnonymousPlatform = AnonymousPlatform"]},
    install_requires=["FlaskBB>=2.1.0"],

)
