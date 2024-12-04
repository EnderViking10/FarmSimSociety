from setuptools import setup, find_packages

setup(
    name="database",
    version="1.0.0",
    description="FSS Database utils",
    author="Erik Klem",
    packages=find_packages(),
    install_requires=[
        "flask",
        "sqlalchemy",
        "flask-login",
    ],
)
