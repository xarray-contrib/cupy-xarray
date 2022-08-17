import setuptools
import versioneer

with open("README.md", "r") as fh:
    long_description = fh.read()
with open("requirements.txt", "r") as fh:
    requirements = [line.strip() for line in fh]

setuptools.setup(
    name="cupy-xarray",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="cupy-xarray developers",
    description="Interface for using cupy in xarray, providing convenience accessors.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "xarray.backends": ["kvikio=cupy_xarray.kvikio:KvikioBackendEntrypoint"],
    },
)
