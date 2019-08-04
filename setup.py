from setuptools import setup, find_packages

setup(
    packages=find_packages(exclude='tests'),
    tests_require=['pytest', 'werkzeug', 'click'],
    install_requires=['click', 'werkzeug'],
    entry_points={
        'console_scripts': [
            'cwmock=cwmock.__main__:main'
        ],
    }
)
