from setuptools import setup, find_packages

requires = [
    'flask',
    'flask_cors', 
    'flask_login'
    'logzero'
    'pymongo',
    'requests',
    'requests_futures',
    'bcrypt',
]

setup(
    name='nerdherd_backend',
    version='0.1',
    description='Backend services for NerdHerd\' DevC Final Project',
    author='MinhTu Thomas Hoang',
    author_email='minhtu.hoang19@gmail.com',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)