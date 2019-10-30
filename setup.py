import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hbi_datagen",
    version="0.0.3",
    author="Brandon Tweed",
    author_email="zbrandontweed@gmail.com",
    description="Package to generate example payloads for consumption by the HBI service.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/catastrophe-brandon/hbi-datagen",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
