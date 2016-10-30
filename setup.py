from setuptools import setup
from cruijff.constants import __version__


DESC = """
TBD
"""


setup(
    name="cruijff",
    version=__version__,
    author="myyc",
    description="Some football data",
    license="BSD",
    keywords="data mining football python pandas mysql mongodb",
    packages=["cruijff"],
    long_description=DESC,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires=["requests", "pandas", "redis", "bs4", "sqlalchemy",
                      "mysqlclient", "appdirs", "pymongo"],
)
