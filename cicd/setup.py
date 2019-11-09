from setuptools import setup, find_packages


with open("README.md") as fp:
    long_description = fp.read()

__version__ = "0.0.10"

setup(
    name="onema-cdk.cicd-pipelines",
    version=__version__,

    description="Constructs to deploy CICD pipelines using CodePipeline and CodeBuild",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Juan Manuel Torres",
    author_email="software@onema.io",
    url="https://github.com/onema/cdk-constructs",   # project home page, if any
    project_urls={
        "Bug Tracker": "https://github.com/onema/cdk-constructs/issues",
        "Documentation": "https://github.com/onema/cdk-constructs",
        "Source Code": "https://github.com/onema/cdk-constructs",
    },

    packages=find_packages(exclude=["ez_setup", "test", "test.*"]),

    install_requires=[
        "aws-cdk.core",
        "aws-cdk.aws-codebuild",
        "aws-cdk.aws-codepipeline",
        "aws-cdk.aws-codepipeline-actions",
        "aws-cdk.aws-ssm",
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
