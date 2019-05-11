from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="cumtime",
    version="0.3.0",
    description="Cumulative measurement of execution time",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atsuoishimoto/cumtime.py",
    author="Atsuo Ishimoto",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords="cumtime",
    py_modules=["cumtime"],
    python_requires=">=3.6",
    project_urls={
        "Bug Reports": "https://github.com/atsuoishimoto/cumtime.py/issues",
        "Source": "https://github.com/atsuoishimoto/cumtime.py",
    },
)
