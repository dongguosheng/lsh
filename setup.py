from distutils.core import setup

setup(
    name = 'lsh',
    packages = ['lsh'], # the same as the name above
    version = '0.1.0',
    description = 'locality-sensitive hashing index, learning to hash',
    author = 'Dong Guosheng',
    author_email = 'dongguosheng179@gmail.com',
    url = 'https://github.com/dongguosheng/lsh', # URL to the github repo
    download_url = 'https://github.com/dongguosheng/lsh/tarball/0.1.0',
    install_requires=['numpy', 'bitarray'],
    keywords = ['lsh', 'locality-sensitive hash', 'learning to hash'],
    classifiers = [],
)
