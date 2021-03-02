from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Unofficial Otter.ai Python API'

setup(
        name="otterai", 
        version=VERSION,
        author="Chad Lohrli",
        description=DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            'requests',
            'requests_toolbelt'
        ],
        keywords=['python', 'otterai', 'api']
)