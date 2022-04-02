# Petri-Net-Simulation

In this section, we implemented a Petri net visualization to illustrate clearly how, the system work. We used multi-purposes language Python in to implement this because their are some helpful library that we can use to draw the graph and to show the animation on the window.
We want to introduce to you that there are at least 4 file in the package: petriNet.py, place.py, transition.py, ⟨input_file_name⟩.txt
We want to give a brief introduction about the input file form as below:

PLACES <number of place>
<placeID>
<input transition1>,<input transition2>,...
<output transition1>,<output transition2>,...
<initial number of token>
<xAxis>,<yAxix>
<placeID>
<input transition1>,<input transition2>,...
<output transition1>,<output transition2>,...
<initial number of token>
<xAxis>,<yAxix>
. 
.
.
TRANSITIONS <number of transition>
<transitionID>
<input place1>,<input place2>,...
<output place1>,<output place2>,...
<xAxis>,<yAxix>
<transitionID>
<input place1>,<input place2>,...
<output place1>,<output place2>,...
<xAxis>,<yAxix>
.
. 
.
