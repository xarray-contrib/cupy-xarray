import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
with open("requirements.txt", "r") as fh:
    requirements = [line.strip() for line in fh]

setuptools.setup(
    name="cupy-xarray",
    version="0.0.1",
    author="Jacob Tomlinson",
    author_email="jtomlinson@nvidia.com",
    description="Interface for using cupy in xarray, providing convenience accessors.",
    long_description=long_description,
    long_description_content_type="text/x-markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
)