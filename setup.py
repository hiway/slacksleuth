from setuptools import setup, find_packages

setup(
    name='slacksleuth',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'plumbum',
        'requests',
        'pyobjc',
        'slackclient',
        'py-applescript',
    ],
    entry_points='''
    [console_scripts]
    slacksleuth=slacksleuth.cli:cli
    ''',
)
