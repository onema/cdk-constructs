from setuptools import setup, find_packages


with open("README.md") as fp:
    long_description = fp.read()

__version__ = "0.0.10"

setup(
    name="onema-cdk.static-website",
    version=__version__,

    description="A CDK Python construct to create static S3 websites. This is a port of the AWS static site example https://github.com/aws-samples/aws-cdk-examples/blob/master/typescript/static-site/static-site.ts",
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
        "aws-cdk.aws-events",
        "aws-cdk.aws-events-targets",
        "aws-cdk.aws-certificatemanager",
        "aws-cdk.aws-cloudfront",
        "aws-cdk.aws-route53",
        "aws-cdk.aws-route53-targets",
        "aws-cdk.aws-s3",
        "aws-cdk.aws-s3-deployment",
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
