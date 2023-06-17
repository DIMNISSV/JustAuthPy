from setuptools import setup

with open('requirements.txt', encoding='utf-8') as f:
    requires = f.read().strip().splitlines()

setup(
    name='JustAuthPy',
    version='0.0.1',
    packages=['auth_client'],
    url='https://github.com/DIMNISSV/JustAuthPy',
    license='GNU GPL v3.0',
    author='DIMNISSV',
    author_email='dimnissv@yandex.kz',
    description='',
    install_requires=requires
)
