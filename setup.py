import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="VTunit", # Replace with your own username
    version="0.0.1-alpha",
    author="Tony Martinet",
    author_email="tonymartinet@gmail.com",
    description="Unit test helper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vtunr/VTunit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)