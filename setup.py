import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scanapi",
    version="0.0.12",
    author="Camila Maia",
    author_email="cmaiacd@gmail.com",
    description="Automated Testing and Documentation for your REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/camilamaia/scanapi",
    packages=setuptools.find_packages(),
    install_requires=["click >= 7.0", "pyyaml >= 5.1.1", "requests >= 2.22.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points="""
        [console_scripts]
        scanapi = scanapi:scan
    """,
)
