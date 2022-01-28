from setuptools import setup, find_packages
import src


setup(
    name='twitter-lib-for-me',
    version=src.__version__,
    # description='',
    # long_description='',
    # url='',
    # author='',
    # author_email='',
    # license='',
    # classifiers='',
    # keywords='',
    # project_urls={},
    packages=find_packages(),
    install_requires=['tweepy~=4.4.0'],
    python_requires='>=3.10',
)
