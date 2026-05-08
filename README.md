# fluxKit

fluxKit is a python package intended to allow for easy post-processing of blacklight images and simple comparison with AthenaMC spectra. It was originally created as part of an ASTR5460 final project, however has extended use within research. 

You may install bap using the following series of terminal commands
```
git clone https://github.com/thomas-03/blacklightAthenaProcessing.git
cd blacklightAthenaProcessing
python -m pip install -e .
```
If you are using a virtual environment be sure to install it there so that you can use it everywhere.

In this case the base_input_file specifies the majority of the simulation parameters outside of the input file and the output file names. The directory is whichever folder for which you want to image all of the containing .athdf and .phdf files. If you wish to do so and have PyLauncher installed, you may also perform the blacklight simulations with PyLauncher by using the -p flag.

You may also perform the tests from the command-line using the following command.

```

pytest tests/

```

Within the tests/ folder there is also helpful jupyter notebook you may run in order to similarly test the functionality of the code and get an idea of how it may be used.

We acknowledge the use of AI in the development of this code, in particular in helping write some of the test cases and in helping with the overall python package structure and .toml file.

