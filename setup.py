from os.path import abspath, dirname, join
from setuptools import setup, find_packages

HERE = dirname(abspath(__file__))

PKG_NAME = "norbi"

info = {}
init_file = join(HERE, PKG_NAME, "__init__.py")
exec(open(init_file).read(), globals(), info)


def read(fname):
    """ Returns content of the passed file.
    """
    return open(join(HERE, fname)).read()


setup(
    name=PKG_NAME,
    version=info["__version__"],
    author="Brent Kendrick",
    author_email="bkendrick@kbibiopharma.com",
    license="Proprietary",
    url="http://www.kbibiopharma.com/",
    description="HPLC data analysis tool",
    long_description=read("README.md"),
    ext_modules=[],
    packages=find_packages(),
    install_requires=["pandas", "numpy", "matplotlib", "scipy", "peakutils"],
    requires=[],
    # Additional data files
    data_files=[(".", ["README.md"])],
    entry_points={},
)
