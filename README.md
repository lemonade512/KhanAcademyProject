<h1>Setup</h1>
In order to run the visualization you must first install a few libraries.

<h3>setuptools</h3>
The NodeBox installation process requires that python's setuptools module be installed.
Go to  https://pypi.python.org/pypi/setuptools and follow the instructions for your OS.

<h3>Pyglet</h3>
Pyglet is needed for NodeBox to work so install that first. To install Pyglet,
go to http://www.pyglet.org/download.html and install the proper file for your OS.
As of right now pyglet is on release 1.1.4 so install that version.

<h3>NodeBox</h3>
With pyglet installed, you can now install NodeBox from http://www.cityinabottle.org/nodebox/.
I am working with the 1.7 release. Install the archive for that release and unzip it somewhere. Once
it is unzipped, open up a terminal inside the new folder then run the command:

        python setup.py install

This should install nodebox to your machine and the visualization should work correctly.