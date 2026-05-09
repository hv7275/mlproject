from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements(file_path: str) -> List[str]:
    '''
    This function will return the list of requirements
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        # Remove newlines
        requirements = [req.replace("\n", "") for req in requirements]

        # Remove '-e .' if it exists in requirements.txt
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    
    return requirements # Crucial: Don't forget to return the list!

setup(
    name='mlproject',
    version='0.0.1',
    author='Harsh',
    author_email='hv7275384@gmail.com',
    packages=find_packages(), 
    install_requires=get_requirements('requirements.txt')
)