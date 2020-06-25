import setuptools

requirements = [
    "click >= 7.0",
    "curlify >= 2.2.1",
    "jinja2 >= 2.10.3",
    "pyyaml >= 5.1.1",
    "requests >= 2.22.0",
]
dev_requirements = ["black >= 19.10b0", "ipdb >= 0.13.2", "pre-commit >= 1.20.0"]
test_requirements = [
    "codecov >= 2.0.15",
    "pytest >= 5.2.4",
    "pytest-cov >= 2.8.1",
    "pytest-freezegun >= 0.4.1",
    "pytest-mock >= 1.11.2",
    "requests-mock >= 1.7.0",
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scanapi",
    version="1.0.1",
    author="Camila Maia",
    author_email="cmaiacd@gmail.com",
    description="Automated Testing and Documentation for your REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scanapi/scanapi",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    extras_require={"dev": dev_requirements, "test": test_requirements},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points="""
        [console_scripts]
        scanapi = scanapi:main
    """,
    zip_safe=False,
    include_package_data=True,
    package_data={"scanapi": ["scanapi/templates/*"]},
)
