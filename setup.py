from setuptools import setup


setup(
    name="disbursement_calculator",
    version="1.0",
    install_requires=[
        "pandas",
        "pandera",
        "openpyxl",
        "tabulate",
        "parameterized",
    ],
    package_data={
        "": ["**/*"],
    },
    package_dir={
        "": "python/",
    },
    packages=["disbursement_calculator"],
)
