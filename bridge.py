class Bridge:
    def __init__(self,name,printTrace):
        self.name=name
        self.lans=set()
        self.root=self

        self.printTrace=printTrace

        self.changed=False
        self.rp=None
        self.dp=set()
        self.distance=0
        self.trace=list()
        self.transmits=False
        self.next=None

    def newConnection(self,lan):
        self.lans.add(lan)
        self.dp.add(lan)

    def sendMessage(self, time):
        if self.root is self or self.transmits:
            if self.printTrace:
                self.trace.append(f'{time} s {self.name} ({self.root.name} {self.distance} {self.name})')
            for lan in self.lans:
                lan.sendMessage((self.root, self.distance, self), time)
            self.changed = False
            self.transmits = False

    def receiveMessage(self, message, lan, time):
        root, distance, bridge = message

        if self.printTrace:
            self.trace.append(f'{time+1} r {self.name} ({root.name} {distance} {bridge.name})')

        if self.distance > distance or (self.distance == distance and self.name > bridge.name):
            if lan in self.dp:
                self.dp.remove(lan)
                self.changed = True

        distance += 1

        if root.name > self.root.name or (root.name == self.root.name and distance > self.distance):
            return
        if self.next:
            if root.name == self.root.name and distance == self.distance and bridge.name > self.next.name:
                return

        self.changed = True
        self.transmits = True
        self.root = root
        self.distance = distance
        self.rp = lan
        self.next = bridge


    def isActive(self, lan):
        return self.rp is lan or lan in self.dp

    def display(self):
        print('{}: {}'.format(self.name, self.lans))

class Lan:
    def __init__(self, name):
        self.name = name
        self.bridges = set()

    def newConnection(self, bridge):
        self.bridges.add(bridge)


    def sendMessage(self, message, t):
        sender = message[2]

        for bridge in self.bridges:
            if bridge is not sender:
                bridge.receiveMessage(message, self, t)

    def display(self):
        print('{}: {}'.format(self.name, self.bridges))

class STP:
    def __init__(self,input_filename,output_filename=None):
        self.BRIDGES={}
        self.LANS={}
        self.flag=True
        self.output=list()
        self.input_filename=input_filename
        if output_filename is not None:
            self.output_filename=output_filename
        else:
            self.output_filename=None

    def parseInput(self,inp):
        inputs = inp.split()
        return inputs[0][:-1], inputs[1:]

    def initialize(self):
        file = open(self.input_filename,"r")
        self.flag=int(file.readline())
        n = int(file.readline())
        for i in range(n):
            bridge, lans = self.parseInput(file.readline())
            self.BRIDGES[i] = Bridge(bridge, self.flag)
            for lan in lans:
                if lan not in self.LANS:
                    self.LANS[lan] = Lan(lan)
                self.BRIDGES[i].newConnection(self.LANS[lan])
                self.LANS[lan].newConnection(self.BRIDGES[i])
        file.close()

    def generateSpanningTree(self):
        loop  = True
        time = 1

        while loop:
            # send or forward config messages from bridges
            for i in self.BRIDGES:
                self.BRIDGES[i].sendMessage(time)
            time += 1

            # check if some bridge was mutated
            loop = False
            for i in self.BRIDGES:
                if self.BRIDGES[i].changed:
                    loop = True
                    break

        # print trace output
        if self.flag:
            trace = []

            for i in self.BRIDGES:
                trace.extend(self.BRIDGES[i].trace)
                self.BRIDGES[i].trace.clear()
            self.output.append('\n'.join(sorted(trace)))


        # print required output
        for i in range(len(self.BRIDGES)):
            bridge = self.BRIDGES[i]
            output = []

            for lan in bridge.lans:
                if bridge.rp is lan:
                    output.append(f'{lan.name}-RP')
                elif lan in bridge.dp:
                    output.append(f'{lan.name}-DP')
                else:
                    output.append(f'{lan.name}-NP')

            self.output.append(f'{bridge.name}: ' + ' '.join(sorted(output)))

    def printOutput(self):
        for i in self.output:
            print(i)

    def writeOutput(self):
        if self.output_filename:
            opfile = open(self.output_filename,"w")
            for i in self.output:
                print(i,file=opfile)
            opfile.close()
