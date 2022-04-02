class Transition():
    def __init__(self, id = 0, inputs = None, outputs = None, position = [0,0]):
        self.id = id

        if inputs is None:
            self.M = 0
            self.inputs = []
        else:
            self.M = len(inputs)
            self.inputs = inputs

        if outputs is None:
            self.N = 0
            self.outputs = []
        else:
            self.N = len(outputs)
            self.outputs = outputs
            
        self.position = position

    def __str__(self):
        return "\"" + str(self.id) + "\""

    def add_input(self, input):
        self.inputs.append(input)
        self.M = len(self.inputs)

    def add_output(self, output):
        self.outputs.append(output)
        self.N = len(self.outputs)

    def set_position(self, pos):
        self.position = pos

    def isEnable(self):
        print("- CHECKING TRANSITION: " + str(self))
        enable = True
        for place in self.inputs:
            if not place.ready():
                print("   > " + str(place) + " is not ready.")
                enable = False
            else:
                print("   > " + str(place) + " is ready!")
        return enable

    def fire(self):
        print("- FIRE TRANSITION: " + str(self))
        for place in self.inputs:
            place.output()
            print("   > 1 token consumed from " + str(place))
        for place in self.outputs:
            place.input()
            print("   > 1 token produced to " + str(place))