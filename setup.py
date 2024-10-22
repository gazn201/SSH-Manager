from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Easy ssh managment tool'
setup(
       # the name must match the folder name 'verysimplemodule'
        name="ssh-manager", 
        version=VERSION,
        description=DESCRIPTION,
        packages=find_packages(),
        scripts=['ssh-manager'],
        install_requires=['python-dotenv',
            'argparse',
            'ipaddress',
            'pyreadline',
            'environ',
            'pyyaml',
            ], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'


)
