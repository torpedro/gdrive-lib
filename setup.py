from setuptools import setup, find_packages

import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="gdrive_lib",
    version="0.0.1",
    description="",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/torpedro/gdrive-lib",
    license="MIT",
    packages=["gdrive_lib"],
    include_package_data=True,
    install_requires=[
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        "oauth2client",
        "mypy",
        "pylint"
    ],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    }
)