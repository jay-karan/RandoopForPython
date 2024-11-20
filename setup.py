from setuptools import setup, find_packages

setup(
    name="randoop-cli",
    version="1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "randoop-cli = randoop_cli.clinew:main",
        ]
    },
    install_requires=[],
    author="Your Name",
    description="Randoop-style test generator for Python classes",
)
