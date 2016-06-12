#!/usr/bin/env python

from setuptools import setup
from pip.req import parse_requirements

requirements_txt = './requirements.txt'
requires = [str(r.req) for r in parse_requirements(requirements_txt, session=False)]

setup(
    name='linebot',
    version='0.3',
    packages=['linebot'],
    install_requires=requires,
    author='Satoshi SUZUKI',
    author_email='studio3104.com@gmail.com',
    description=('A client library for LINE BOT'),
    license='MIT',
    url='https://github.com/studio3104/line-bot-sdk-python',
)
