from setuptools import setup, find_packages


def readme():
    with open("README.md") as f:
        return f.read()


install_requires = ["geopandas==0.10.2", "scipy==1.7.3"]

setup(
    name="geobootstrap",
    version="0.1",
    description="Python tools for geobootstrapping",
    long_description=(readme()),
    long_description_content_type="text/markdown",
    url="https://github.com/tastatham/geobootstrap",
    author="Thomas Statham",
    author_email="tastatham@gmail.com",
    keywords="bootstrap, spatial",
    license="MIT",
    packages=find_packages(exclude=["tests"]),
    install_requires=install_requires,
    include_package_data=False,
)
