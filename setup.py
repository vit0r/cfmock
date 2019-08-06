from setuptools import setup, find_packages

setup(
    packages=find_packages(exclude='tests'),
    tests_require=['pytest==5.0.1', 'werkzeug==0.15.5', 'click==7.0'],
    install_requires=['werkzeug==0.15.5', 'click==7.0'],
    entry_points={
        'console_scripts': [
            'cwmock=cwmock.__main__:main'
        ],
    }
)
