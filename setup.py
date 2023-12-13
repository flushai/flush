from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.4'
DESCRIPTION = 'SDK for Flush AI (flushai.cloud)'
LONG_DESCRIPTION = 'A package that allows you to easily generate images and gifs using animate diff, stable diffusion, civit-ai, and many other popular image generation models.'

# Setting up
setup(
    name="flushai",
    version=VERSION,
    author="Flush AI inc.",
    author_email="saketh.kotamraju@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
    "requests",
    "dropbox==11.36.2",
    "PyMuPDF",
    "google_api_python_client==2.104.0",
    "google_auth_oauthlib==1.1.0",
    "opencv_python==4.8.0.74",
    "pexels_api==1.0.1",
    "Pillow==9.4.0",
    "Pillow==10.1.0",
    "pillow_heif==0.13.1",
    "protobuf==4.25.0",
    "pytube==15.0.0",
    "Requests==2.31.0",
    "setuptools==68.2.2",
    "pillow-heif",
    "google-search-results",
    "openai",
    "pytube"

],
    keywords=['python', 'image generation', 'flush ai', 'stable diffusion', 'civit ai', 'animatediff'], 
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)