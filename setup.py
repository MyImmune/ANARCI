import shutil, os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from setuptools.command.install import install


with open('requirements.txt') as f:
    required = f.read().splitlines()

class CustomInstallCommand(install):
   def run(self):
        install.run(self)
        # Post-installation routine — use self.install_lib/install_scripts so
        # this works correctly for --user, venv, conda, and system installs.
        ANARCI_LOC = os.path.join(self.install_lib, 'anarci')
        if os.path.exists(ANARCI_LOC) and not os.path.isdir(ANARCI_LOC):
            os.remove(ANARCI_LOC)
        os.makedirs(ANARCI_LOC, exist_ok=True)
        shutil.copy("curated_alignments/germlines.py", ANARCI_LOC)
        print("INFO: ANARCI lives in: ", ANARCI_LOC)
        destination = os.path.join(ANARCI_LOC, "dat/HMMs/")
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        if os.path.exists(destination):
            shutil.rmtree(destination)
        shutil.copytree("HMMs", destination)


setup(name='anarci',
     version='1.3',
     description='Antibody Numbering and Receptor ClassIfication',
     install_requires=required,
     author='James Dunbar',
     author_email='opig@stats.ox.ac.uk',
     url='http://opig.stats.ox.ac.uk/webapps/ANARCI',
     packages=['anarci'],
     package_dir={'anarci': 'lib/python/anarci'},
     data_files = [ ('bin', ['bin/muscle', 'bin/muscle_macOS']) ],
     include_package_data = True,
     scripts=['bin/ANARCI'],
     cmdclass={"install": CustomInstallCommand, }, # Run post-installation routine
    )
