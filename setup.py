from setuptools import find_packages, setup
from typing import List
from distutils.core import setup

HYPHEN_E = '-e .'
def get_requirement(filepath: str)->List[str]:
    requirements = []

    with open(filepath) as file:
        requirements = file.readlines()
    requirements = [r.replace("\n", "") for r in requirements]

    if HYPHEN_E in requirements:
        requirements.remove(HYPHEN_E)



setup(name='ML-Pipeline',
      version='0.0.1',
      description='End-to-End ML Pipeline',
      author='Aakash Agarwal',
      author_email='aakash24@seas.upenn.edu',
      packages=get_requirement("requirements.txt"),
     )