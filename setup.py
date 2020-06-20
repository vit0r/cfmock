"""
Setup install or test
"""
from setuptools import find_packages, setup

setup(
    packages=find_packages(exclude="tests"),
    tests_require=[
        "pytest==5.0.1",
        "werkzeug==0.15.5",
        "click==7.0",
        "tinymongo==0.1.9",
    ],
    install_requires=["werkzeug==0.15.5", "click==7.0", "tinymongo==0.1.9"],
    entry_points={"console_scripts": ["dynomock=dynomock.__main__:main"],},
)
