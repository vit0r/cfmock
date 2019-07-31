from setuptools import setup, find_packages

setup(
    packages=find_packages(exclude='tests'),
    tests_require=['ptest', 'flask', 'click'],
    install_requires=['click', 'flask'],
    entry_points={
        'console_scripts': [
            'cfmock=cfmock.__main__:main'
        ],
    }
)
