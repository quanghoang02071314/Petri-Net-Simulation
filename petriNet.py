import sys
import math
from random import shuffle
from matplotlib import pyplot as plt
from matplotlib import animation
from place import Place as Place
from transition import Transition as Transition

global transitionSize
global placeSize
global tokenSize

transitionSize = 3
placeSize = 1.5
tokenSize = 0.15
maxNumOfTokenInAPlace = 10

# Read text file function


def readFromFile(filename, place_tuples, transition_tuples):
    file = open(filename, 'r')

    num_places = int((file.readline()).split(" ")[1].rstrip('\n'))
    for i in range(num_places):
        file.readline()
        place_id = file.readline().rstrip('\n')
        place_inputs = [input.rstrip('\n')
                        for input in file.readline().split(",")]
        place_outputs = [output.rstrip('\n')
                         for output in file.readline().split(",")]
        place_tokens = int(file.readline().rstrip('\n'))
        place_position = tuple([int(coordinate.rstrip('\n'))
                               for coordinate in file.readline().split(",")])
        # If there are any place has initial number of token smaller than 0
        # ==> Print out error and terminate the program.
        if(place_tokens < 0):
            print("ERROR: Initial token of a place cannot smaller than 0!")
            sys.exit()
        place_tuple = (place_id, place_inputs, place_outputs,
                       place_tokens, place_position)
        place_tuples.append(place_tuple)
    file.readline()

    # If there are any place has initial number of token greater than maximum number of token in a place which was defined
    # ==> Print out error and terminate the program.
    for place in place_tuples:
        if(place[0] == 'wait' and place[3] > maxNumOfTokenInAPlace):
            print("ERROR: Initial token of place \"wait\" cannot greater than {}!".format(
                maxNumOfTokenInAPlace))
            sys.exit()

    num_transitions = int((file.readline()).split(" ")[1].rstrip('\n'))
    for i in range(num_transitions):
        file.readline()
        transition_id = file.readline().rstrip('\n')
        transition_inputs = [input.rstrip('\n')
                             for input in file.readline().split(",")]
        transition_outputs = [output.rstrip('\n')
                              for output in file.readline().split(",")]
        transition_position = tuple(
            [int(coordinate.rstrip('\n')) for coordinate in file.readline().split(",")])
        transition_tuple = (transition_id, transition_inputs,
                            transition_outputs, transition_position)
        transition_tuples.append(transition_tuple)
    file.close()

# Initializing function


def initialize(place_tuples, transition_tuples, places, transitions):
    # initialize places
    for tuple in place_tuples:
        place = Place(tuple[0])
        place.add_tokens(tuple[3])
        place.set_position(tuple[4])
        places.append(place)
    # initialize transition objects
    for tuple in transition_tuples:
        transition = Transition(tuple[0])
        transition.set_position(tuple[3])
        transitions.append(transition)
    # add transition objects to place inputs/outpus
    for i in range(len(places)):
        for input_id in place_tuples[i][1]:
            for transition in transitions:
                if input_id == transition.id:
                    places[i].add_input(transition)
        for output_id in place_tuples[i][2]:
            for transition in transitions:
                if output_id == transition.id:
                    places[i].add_output(transition)
    # add place objects to transition inputs/outputs
    for i in range(len(transitions)):
        for input_id in transition_tuples[i][1]:
            for place in places:
                if input_id == place.id:
                    transitions[i].add_input(place)
        for output_id in transition_tuples[i][2]:
            for place in places:
                if output_id == place.id:
                    transitions[i].add_output(place)


# Read input file and initialize places and transitions
place_tuples = []
transition_tuples = []
readFromFile(sys.argv[1], place_tuples, transition_tuples)
places = []
transitions = []
initialize(place_tuples, transition_tuples, places, transitions)

######## Preparing figure ########
# Initialize plot
maxX = -99999
minX = 99999
maxY = -99999
minY = 99999
for place in places:
    if maxX < place.position[0]:
        maxX = place.position[0]
    if minX > place.position[0]:
        minX = place.position[0]
    if maxY < place.position[1]:
        maxY = place.position[1]
    if minY > place.position[1]:
        minY = place.position[1]
for transition in transitions:
    if maxX < transition.position[0]:
        maxX = transition.position[0]
    if minX > transition.position[0]:
        minX = transition.position[0]
    if maxY < transition.position[1]:
        maxY = transition.position[1]
    if minY > transition.position[1]:
        minY = transition.position[1]
fig = plt.figure()
fig.canvas.manager.set_window_title('Petri Net Visialization: ' + sys.argv[1])
fig.set_dpi(100)
fig.set_size_inches(maxX - minX + 2.4*transitionSize,
                    maxY - minY + 2.4*transitionSize)
ax = plt.axes(xlim=(minX-4, maxX+4), ylim=(minY-4, maxY+4))

# Create place, token & transition patches
place_patches = []
token_patches = []
place_labels = []

for place in places:
    place_patch = plt.Circle(place.position, placeSize,
                             ec='black', fc='white', lw=2, zorder=0)
    place_patches.append(place_patch)
    for i in range(maxNumOfTokenInAPlace):
        row = i//5
        token_patch = plt.Circle((place.position[0] + ((i % 5)-2)*tokenSize*3, place.position[1] + (
            maxNumOfTokenInAPlace//5//2-row)*tokenSize*3), tokenSize, fc='black', zorder=1)
        token_patches.append(token_patch)

transition_patches = []
for transition in transitions:
    transition_patch = plt.Rectangle(
        (transition.position[0]-transitionSize/2,
         transition.position[1]-transitionSize/2),
        transitionSize, transitionSize, fc='white', ec='black', lw=2
    )
    transition_patches.append(transition_patch)

# Drawing flow relations


def distance(source, target):
    return math.sqrt((target.position[0] - source.position[0])**2 + (target.position[1] - source.position[1])**2)


def drawArrow(source, target):
    if -(math.sqrt(2)/2)*distance(source, target) < target.position[0] - source.position[0] and target.position[0] - source.position[0] < (math.sqrt(2)/2)*distance(source, target):
        if source.position[1] < target.position[1]:
            outputFace = 1
        else:
            outputFace = 3
    else:
        if source.position[0] < target.position[0]:
            outputFace = 0
        else:
            outputFace = 2

    if type(source) is Place:
        # Truncate arrow distance slightly to display head and tail
        if outputFace == 0:
            start_pos = (source.position[0] + placeSize, source.position[1])
            end_pos = (target.position[0] -
                       transitionSize/2, target.position[1])
        elif outputFace == 1:
            start_pos = (source.position[0], source.position[1] + placeSize)
            end_pos = (target.position[0],
                       target.position[1] - transitionSize/2)
        elif outputFace == 2:
            start_pos = (source.position[0] - placeSize, source.position[1])
            end_pos = (target.position[0] +
                       transitionSize/2, target.position[1])
        elif outputFace == 3:
            start_pos = (source.position[0], source.position[1] - placeSize)
            end_pos = (target.position[0],
                       target.position[1] + transitionSize/2)
    else:
        # Truncate arrow distance slightly to display head and tail
        if outputFace == 0:
            start_pos = (source.position[0] +
                         transitionSize/2, source.position[1])
            end_pos = (target.position[0] - placeSize, target.position[1])
        elif outputFace == 1:
            start_pos = (source.position[0],
                         source.position[1] + transitionSize/2)
            end_pos = (target.position[0], target.position[1] - placeSize)
        elif outputFace == 2:
            start_pos = (source.position[0] -
                         transitionSize/2, source.position[1])
            end_pos = (target.position[0] + placeSize, target.position[1])
        elif outputFace == 3:
            start_pos = (source.position[0],
                         source.position[1] - transitionSize/2)
            end_pos = (target.position[0], target.position[1] + placeSize)

    plt.arrow(
        start_pos[0], start_pos[1],
        end_pos[0] - start_pos[0], end_pos[1] - start_pos[1],
        length_includes_head=True,
        fc='black', ec='black', head_width=placeSize*0.2, head_length=placeSize*0.3
    )


def init():
    # add tokens
    for i in range(len(token_patches)):
        ax.add_patch(token_patches[i])
    # add places
    for i in range(len(place_patches)):
        ax.add_patch(place_patches[i])
        ax.text(
            places[i].position[0] - placeSize*0.5,
            places[i].position[1] - placeSize*1.3,
            places[i].id,
            horizontalalignment='center',
            fontsize=20
        )
        # set token patch visible if place has token
        for j in range(maxNumOfTokenInAPlace):
            if j < places[i].tokens:
                token_patches[i*maxNumOfTokenInAPlace + j].set_visible(True)
            else:
                token_patches[i*maxNumOfTokenInAPlace + j].set_visible(False)

    # add all transition patches
    for i in range(len(transition_patches)):
        ax.add_patch(transition_patches[i])
        ax.text(
            transitions[i].position[0],
            transitions[i].position[1] - transitionSize*0.7,
            transitions[i].id,
            horizontalalignment='center', fontsize=20
        )
        # add input arrows
        for input in transitions[i].inputs:
            drawArrow(input, transitions[i])
        # add output arrows
        for output in transitions[i].outputs:
            drawArrow(transitions[i], output)
    return token_patches


num_of_fires = 0
step = 0
firedTransition = transitions[0]
fire = True


def animate(i):
    global fire
    global step
    global num_of_fires
    global firedTransition
    if fire == True:
        if step == 0:
            print("\n==== INITIALIZATION ===")
        else:
            print("\n======= STEP #{} =======".format(step))
            firedTransition.fire()
            num_of_fires += 1

        for i in range(len(place_patches)):
            for j in range(maxNumOfTokenInAPlace):
                if j < places[i].tokens:
                    token_patches[i*maxNumOfTokenInAPlace +
                                  j].set_visible(True)
                else:
                    token_patches[i*maxNumOfTokenInAPlace +
                                  j].set_visible(False)
        print(
            "- THE MARKING OF STEP #{} IS: [".format(step),
            ', '.join(place.marking() for place in places if place.tokens > 0),
            "]"
        )

        shuffle(transitions)
        for transition in transitions:
            if transition.isEnable():
                firedTransition = transition
                fire = True
                break
            fire = False

        step += 1
    return token_patches


anim = animation.FuncAnimation(
    fig, animate,
    init_func=init,
    frames=500,
    interval=1500
)

print("========== PETRI NET ANIMATION ==========")
plt.show()
summary = "\n========== SUMARY ==========\n"
summary += "Final marking: ["
summary += ', '.join(place.marking() for place in places if place.tokens > 0)
summary += "]\n"
summary += "Total fires: " + str(num_of_fires) + "\n"
summary += "Exiting program.\n"
print(summary)
