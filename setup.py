"""
Setup install or test
"""
from setuptools import find_packages, setup

setup(
    packages=find_packages(exclude="tests"),
    tests_require=[
        "pytest==5.4.3",
        "Werkzeug==1.0.1",
        "click==7.1.2",
        "tinydb==4.1.1",
    ],
    install_requires=["werkzeug==0.15.5", "click==7.1.2", "tinydb==4.1.1"],
    entry_points={"console_scripts": ["dynomock=dynomock.__main__:main"], },
)
