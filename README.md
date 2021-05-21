![](img_output.gif)

Code repository for the simulations used of the paper
"Collaborative Intrusion Detection for Large Autonomous Drone Swarms"
submitted to CRITIS 2021

# Instructions to run
The code is written in Python 3.0 and requires the libraries Numpy and Pygame in order to run. 
runner.py is the most obvious starting point for testing and visualizing the simulations. 
However, runner.py was not used to generate research data. All files for generating research data can be found in the "results" folder, along with some generated data sets.

# Structure of Code
The simulations are carried out by mainly in 5 of the files:
* world.py
* bird.py
* tracer.py
* intruder.py
* layouts.py

Again, while runner.py is a recommended starting point for testing the code, it does not contain any simulation code except for visualization.

world.py defines World objects, used to manage all world objects. World objects are typically initialized from the layout.py file, where the different layouts and their initial condiations are defined.
bird.py defines the Bird class, which carries out the main flocking algorithm, and stores position, velocity and neighborhoods for each Bird object.
tracer.py defines the Tracer class, responsible to the CID algorithm. The track() function is intended to run once each timestep, and carry out relevant work. It is also responsible for drawing the bottom part of the simulation window of runner.py
intruder.py defines the intruder types. Only Follower and NonFlocker were used to generate results.

# Notes
The code is actively being worked on, but I intend to freeze a version if the submission is accepted. 
There are many fragments of code that don't serve any current function, but has been used to debug/experiment
The structure may seem needlessly overcomplicated in places, but keep in mind that not only does the code carry out the flocking algorithm, but it also collects and analyzes data about the state of the simulation at every timestep.

# Future work
The ability of coordinated attackers to disrupt flocks will be explored, and hopefully some useful bounds on number attackers needed can be derived and experimentally verified.

![](cut.webm)



