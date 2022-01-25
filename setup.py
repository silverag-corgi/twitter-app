from setuptools import setup, find_packages
import src


setup(
    name='twitter-lib-for-me',
    # author='',
    # author_email='',
    # maintainer='',
    # maintainer_email='',
    # description='',
    # long_description='',
    # license='',
    # url='',
    version=src.__version__,
    # download_url='',
    python_requires='3.10',
    install_requires=['tweepy~=4.4.0'],
    # extras_require='',
    packages=find_packages(),
    # classifiers=''
)
