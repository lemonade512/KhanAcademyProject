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

<h1>Running Tests</h1>

Once you have gone through all of the steps outlined in the setup section you can clone the
repository and run the unit tests. Once you have cloned the repository, change to the top-level
directory and run the command:

        python -m unittest discover Tests

This should print output saying that the tests ran and were OK (as of right now there are 25 tests).
If you want to see what each test checks for, there are short discriptions in test_user.py and
test_user_network.py.

<h1>Running Visualization</h1>

Once you have verified the tests are all working, you can run the visualization. This is probably the
best way to see how the algorithms work. To run the visualization, use the following command:

        python visual_gui.py

In the bottom left corner of the visualization there is a panel that has a bunch of options to choose from.
The field labeled "INFECT" allows you to specify the number passed to the limited infection algorithm. The color
knobs allow you to specify what color to infect nodes with. The button labeled "Total Infection" or
"Limited Infection" specify what type of algorithm you would like to infect with. To change the algorithm just
click the button. Finally, the "Next Network" button cycles through all the available networks to test with.

To start infecting nodes, just pick your infection type with the button and click on the node you want to infect.
You can also use the mouse to drag the canvas around and get a better view of the network.

<h1>After Thoughts</h1>

<h3>Analysis</h3>

One interesting consequence of the limited infection algorithm is that, if given a high enough target value,
the algorithm seems to infect the central nodes more quickly than the leaf nodes. This is probably because
the algorithm will choose the nodes with the most infected students first, and those nodes tend to be the central nodes

<h3>Possible Improvements</h3>

One possible improvement would be to write a version of limited infection that infects exactly the number of users
that you specify. This would require trying every possible combination of uninfected users to see if infecting a
certain combination would yield the desired number of infections.

Another possible improvement would be to add the ability to zoom the graph in and out so it is easier to look at
larger graphs.