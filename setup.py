from setuptools import setup

with open("README.md") as fh:
    readme_text = fh.read()

with open("LICENSE") as fh:
    license_text = fh.read()

setup(
    name="commutator",
    version="1.0.0",
    description="Decompose an algorithm in commutator notation.",
    long_description=readme_text,
    keywords="commutator",
    url="https://github.com/nbwzx/commutator.py@main",
    author="Zixing Wang",
    author_email="zixingwang.cn@gmail.com",
    license=license_text,
    packages=["commutator"],
)