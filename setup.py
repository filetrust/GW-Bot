import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    version                       = "0.4.4"               , # change this on every release
    name                          = "gw_bot"  ,

    author                        = "Dinis Cruz",
    author_email                  = "dinis.cruz@owasp.org",
    description                   = "Glasswall Security Bot",
    long_description              = long_description,
    long_description_content_type = " text/markdown",
    url                           = "https://github.com/filetrust/GW-Bot",
    packages                      = setuptools.find_packages(),
    classifiers                   = [ "Programming Language :: Python :: 3"   ,
                                      "License :: OSI Approved :: MIT License",
                                      "Operating System :: OS Independent"   ])