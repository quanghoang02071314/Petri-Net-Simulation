# Petri-Net-Simulation

## Introduction

We implemented a Petri net visualization to illustrate clearly how, the system work. We used multi-purposes language Python in to implement this because their are some helpful library that we can use to draw the graph and to show the animation on the window.
We want to introduce to you that there are at least 4 file in the package: petriNet.py, place.py, transition.py, ⟨input_file_name⟩.txt
We want to give a brief introduction about the input file form as below:

```
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
```

## Description

Places and transition are separated by the headers including total number of place and tran- sition to be displayed. 
The PLACES header is followed by places information, separated by a blank line: placeID is name of the place, next line is a list of input transitions name, next line is a list of output transitions name, initial number of token and last line is the position of the place to be displayed in the graph.
The TRANSITIONS header is followed by transitions information, separated by a blank line: transitionID is name of the transition, next line is a list of input places name, next line is a list of output places name and last line is the position of the transition to be displayed in the graph.

# User manual

Run following command in terminal:
```
python3 petriNet.py <input_file_name>.txt
```
