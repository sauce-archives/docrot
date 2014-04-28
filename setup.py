from distutils.core import setup

setup(
    name='docrot',
    version='0.1.0',
    author='Sauce Labs',
    author_email='help@saucelabs.com',
    packages=['docrot'],
    url='http://github.com/saucelabs/docrot/',
    license='LICENSE.txt',
    description='A python library for detecting decaying documentation.',
    long_description=open('README.md').read(),
    install_requires=[
        "gitpython >= 0.1.7",
    ],
    entry_points=dict(
        console_scripts=[
            "docrot = docrot.console:main",
        ],
    ),
)
