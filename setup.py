from setuptools import setup, find_packages

setup(
    name="quicklog",
    version="1.0.1",
    install_requires=["numpy", "click", "progressbar"],
    packages=find_packages(),
)
