import shutil, os
import site, sys
from distutils.core import setup
from setuptools.command.install import install


with open('requirements.txt') as f:
    required = f.read().splitlines()

class CustomInstallCommand(install):
   def run(self):
        install.run(self)
        # Post-installation routine
        ANARCI_LOC = os.path.join(site.getsitepackages()[0], 'anarci') # site-packages/ folder
        ANARCI_BIN = sys.executable.split('python')[0] # bin/ folder
        shutil.copy( "curated_alignments/germlines.py", ANARCI_LOC)
        shutil.copy('bin/ANARCI', ANARCI_BIN) # copy ANARCI executable
        print("INFO: ANARCI lives in: ", ANARCI_LOC)
        destination = os.path.join(ANARCI_LOC, "dat/HMMs/")
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
     data_files = [ ('bin', ['bin/muscle', 'bin/muscle_macOS', 'bin/ANARCI']) ],
     include_package_data = True,
     scripts=['bin/ANARCI'],
     cmdclass={"install": CustomInstallCommand, }, # Run post-installation routine
    )
