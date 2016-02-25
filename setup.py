from setuptools import setup, find_packages

setup(
    name='slacksleuth',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'requests',
        'py-applescript',
    ],
    entry_points='''
    [console_scripts]
    slacksleuth=slacksleuth.cli:cli
    ''',
)
