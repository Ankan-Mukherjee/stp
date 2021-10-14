class Bridge:
    
    '''     
    Each of the bridges present in the network is made an object of this class. Their properties are given below.
    
    Member Variables:
        name - Stores the name of the bridge as a string (B1, B2, ...) 
        lans - Set storing the names of lans (A,B,...) connected to the bridge
        root - Stores the bridge object which is the root of the tree (note that this is NOT the immediate root of the current bridge object, but rather the root of the entire tree)
        printTrace - Flag for printing the trace
        changed - Stores True if the message received by a bridge has changed its root, or distance, else False
        rp - Stores the root port lan of the bridge
        dp - Stores the lans whose ports with the bridge are designated ports
        distance - Stores the distance of the bridge from the root
        trace - Stores the trace to be printed
        transmits - Stores True if and only if the bridge sends a message
        top - Stores the immediate root of the bridge under consideration (i.e., the bridge object whose leaf is the current tree) (note that this is NOT the root of the entire tree)
        
    Member Functions:
        newConnection - Adds a new lan as a connection to the bridge
        sendMessage - Sends a message to its connected lans
        receiveMessage - Receives a message from its adjascent lans and updates its information accrodingly
        display - Prints the bridge name along with its connected lans (for debugging puposes only, actual printing is done in the STP class)
    
    '''
    
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
        self.top=None
        
    def newConnection(self,lan):
        self.lans.add(lan) #Append a new lan object to the set of Lans of the bridge for every new Lan detected
        self.dp.add(lan) #Initially, we set all ports to all lans as designated (DP)
        
    
    def sendMessage(self, time):        
        #We will send a message from the bridge if and only if it is a root (whereby it generates its own message) or if transmission is enabledS
        if self.root is self or self.transmits:
            # If printing trace is enabled, we append the trace to the trace of bridge
            if self.printTrace:
                for _ in self.lans:
                    self.trace.append(f'{time} s {self.name} ({self.root.name} {self.distance} {self.name})')
            # We send the message of the bridge to all its lans        
            for lan in self.lans:
                lan.sendMessage((self.root, self.distance, self), time)
                
            # Since we have just sent messages and not received them yet, changes are not done for the current round. Thus, we set changed and transmit to False after transmitting once    
            self.changed = False
            self.transmits = False
                
                
    def receiveMessage(self, message, lan, time):        
        # Here, the bridge will receive the messages from the lan, which have in turn been transmitted to it by the previous bridge
        
        # Extracting the releveant data from the message
        root, distance, bridge = message
        
        # If printing trace is enabled, we append the trace to the trace of bridge
        if self.printTrace:
            self.trace.append(f'{time+1} r {self.name} ({root.name} {distance} {bridge.name})')

        #This is the condition for updating the information about the lans stored in the bridge. Later in this method, we shall modify the other information of the bridge
        if distance < self.distance or (distance == self.distance and bridge.name < self.name): 
            # Since we have found a message from a "better bridge", the lan under consideration is no longer a designated port of the self bridge
            # Since we have updated bridge information, we set changed to True
            if lan in self.dp:
                self.dp.remove(lan)
                self.changed = True

        # Distance is incremented by 1 since the message measured the distance of the sender from the root, so we add sender to receiver distance, which is assumed to be 1
        distance += 1
        
        # If the current bridge is "better" than the bridge sending the message, we do nothing and return 
        if root.name > self.root.name or (root.name == self.root.name and distance > self.distance):
            return
        
        # If the current bridge is not the root of the tree and it is neither "better" nor "worse" than "its" root, we assign the bridge with smaller id (here, name) as the the root of the other
        if self.top:
            if root.name == self.root.name and distance == self.distance and bridge.name > self.top.name:
                return

        # If bridge information were not to be modified, we would have returned by now. Since bridge information is modified, it means the lan sending it is a root port (could be np if and only if the bridge is hanging) and the root, distance and sender of the message become the root, distance+1 and the local root of the self bridge
        self.changed = True
        self.transmits = True
        self.root = root
        self.distance = distance
        self.rp = lan
        self.top = bridge

        
    
    def display(self):
        print('{}: {}'.format(self.name, self.lans))


class Lan:
    
    '''     
    Each of the LANs present in the network is made an object of this class. Their properties are given below.
    
    Member Variables:
        name - Stores the name of the Lan as a string (A, B, ...) 
        bridges - Set storing the names of bridges (B1, B2,...) connected to the lan
        
    Member Functions:
        newConnection - Adds a new bridge as a connection to the lan
        sendMessage - Sends a message to its connected bridges
        display - Prints the lan name along with its connected bridges (for debugging puposes only, actual printing is done in the STP class)
    
    '''
    
    def __init__(self, name):
        self.name = name
        self.bridges = set()

    def newConnection(self, bridge):
        # This is rather straightforward, we are simply appending the bridges connected to the lan to a set
        self.bridges.add(bridge) 


    def sendMessage(self, message, t):
        # We send the message a lan receives from all the bridges connected to it to all the bridges connected to it except the sender
        sender = message[2]
        for bridge in self.bridges:
            if bridge is not sender:
                bridge.receiveMessage(message, self, t)
                
    def display(self):
        print('{}: {}'.format(self.name, self.bridges))


class STP:
    
    '''     
    This class conatins the tree
    
    Member Variables:
        BRIDGES - Stores the bridge objects of the tree
        LANS - Stores the bridge objects of the tree
        flag - Stores flag for printing trace (True or 1 for printing)
        output - Stores the lines

        
    Member Functions:
        parseInput - Separates the input into the bridge and its lans
        initialize - Initializes the bridge and lan objects and the member variables
        generateSpanningTree - Generates the sapnning tree
        printOutput - Prints output to stdout
        writeOutput - Writes output to the output filename
    
    '''
    
    def __init__(self):
        self.BRIDGES={}
        self.LANS={}
        self.flag=True
        self.output=list()
            
    
    def parseInput(self,inp):
        inputs = inp.split()
        return inputs[0][:-1], inputs[1:]
    
    
    def initialize(self):
        # Reading the input from the file
        self.flag=int(input())    
        n = int(input())
        # Storing the bridges and lans
        for i in range(n): 
            bridge, lans = self.parseInput(input())
            self.BRIDGES[i] = Bridge(bridge, self.flag) 
            for lan in lans:
                if lan not in self.LANS:
                    self.LANS[lan] = Lan(lan)
                self.BRIDGES[i].newConnection(self.LANS[lan])
                self.LANS[lan].newConnection(self.BRIDGES[i])

                
    def generateSpanningTree(self):
        #Loop is set to True to start the program. It is set to false inside while and set to True again if any bridge has its changed value as True
        loop  = True
        time = 1

        while loop:
            # Sending messages from each bridge as long as the loop is running
            for i in self.BRIDGES:
                self.BRIDGES[i].sendMessage(time)
            time += 1

            # Checking if any bridge had their values changed
            loop = False
            for i in self.BRIDGES:
                if self.BRIDGES[i].changed:
                    # If any bridge had a change in its parameters, it means the tree is not yet fully setup and loop must continue
                    loop = True
                    break

        # After loop is completed, the tree is fully set-up and each bridge has the final information about the root, distance and the nature of ports
        
        # Now, we are setting up and printing the trace if the flag variable (for trace) was set to True
        if self.flag:
            trace = []

            for i in self.BRIDGES:
                trace.extend(self.BRIDGES[i].trace)
                self.BRIDGES[i].trace.clear()
            self.output.append('\n'.join(sorted(trace)))
        
        
        # This is the output for the type of each port
        for i in range(len(self.BRIDGES)):
            bridge = self.BRIDGES[i]
            output = []
            
            for lan in bridge.lans:
                # A port cannot be both root port and designated port. If it is a root port, it must be removed from the designated ports list
                if lan in bridge.dp and bridge.rp is lan:
                    bridge.dp.remove(lan)
                
            for lan in bridge.lans:
                # If the bridge is a hanging bridge, all its ports are Non-active
                if len(bridge.dp)==0:
                    output.append(f'{lan.name}-NP')
                # If the port is a root port, we print the same    
                elif bridge.rp is lan:
                    output.append(f'{lan.name}-RP')
                # If the port is a desiganted port, we print the same   
                elif lan in bridge.dp:
                    output.append(f'{lan.name}-DP')
                # If the port is neither a root port nor a designated port, it must be non-active    
                else:
                    output.append(f'{lan.name}-NP')

            # Appending this output to the trace
            self.output.append(f'{bridge.name}: ' + ' '.join(sorted(output)))
            
            
            
    def printOutput(self):
        for i in self.output:
            print(i)

