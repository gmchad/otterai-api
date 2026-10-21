from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "Unofficial Otter.ai Python API"

setup(
    name="otterai",
    version=VERSION,
    author="Chad Lohrli",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=["requests>=2.34.2", "requests_toolbelt", "certifi>=2026.10.19"],
    keywords=["python", "otterai", "api"],
)
