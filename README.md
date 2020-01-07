# CITlib
This project is developed by Müge Fidan and Vatan Aksoy Tezer for CS560 - Automated Debugging course in Sabancı University.

The project is known to work with Ubuntu 16.04, Python 3.5.2, Clingo 5.4.0 and only depends on [PyEDA](https://pyeda.readthedocs.io/en/latest/overview.html) and [shc](https://linux.die.net/man/1/shc). To install and use CITlib the following steps should be applied. The installation should work for Debian and OSX based operating systems.

```
$ cd ~ # Go to your home directory
$ git clone https://github.com/vatanaksoytezer/citlib.git # Clone this repository
# cd ~/citlib/
$ sudo make install # Install the binaries
$ source ~/.bashrc # Resource yout environment so you can use the ucit tool right away.
```

To run this tool simply provide a project folder from the command line and CIT coverage will be done for you. The project directory should contain, "user.lp", "coverage_criterion.lp", "testcase.lp" and "system_model.lp" files. The tool can be run as follows:

```
$ ucit PROJECT_DIR
$ sh ~/citlib/ucit.sh PROJECT_DIR # if above command does not work due to system compatibility issues
```