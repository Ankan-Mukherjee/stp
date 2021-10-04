class stp:
    def __init__(self,filename):
        self.BRIDGES=[]
        self.LANS=[]
        self.B_ADJ=dict()
        self.L_B_ADJ=dict()
        self.filename=filename

    def readInput(self):
        file = open(self.filename,"r")
        mode=int(file.readline())
        n=int(file.readline())
        for i in range(n):
            line=file.readline()
            name=line.split(':')[0]
            lans=[lan(x,[]) for x in line.split(':')[1].split()]
            mess=message(name,0,name)
            self.BRIDGES.append(bridge(name,lans,mess))

    def fillLans(self):
        lannames=[]
        for bridge in self.BRIDGES:
            for lan in bridge.lans:
                if lan.name not in lannames:
                    lannames.append(lan.name)
                    self.LANS.append(lan)
        for lan in self.LANS:
            for bridge in self.BRIDGES:
                bridgelans=[x.name for x in bridge.lans]
                if lan.name in bridgelans:
                    lan.bridges.append(bridge)

    def initialize(self):
        self.readInput()
        self.fillLans()
        for bridge in self.BRIDGES:
            for lan in bridge.lans:
                for x in lan.bridges:
                    print(x.name, end=' ')
                    #if x.name!=bridge.name:
                    bridge.adj.append(x)
                print()


    def displayMessage(self,time,type,node,message):
        print('{} {} {}'.format(time,type,node.name),end=' ')
        message.display()

    def sendMessages(self, time):
        for bridge in self.BRIDGES:
            for i in bridge.lans:
                self.displayMessage(time,'s',bridge,bridge.message)

    def receiveMessages(self, time):
        for bridge in self.BRIDGES:
            for i in bridge.lans:
                self.displayMessage(time,'r',bridge,bridge.message)

    def updateMessages():
        for bridge in self.BRIDGES:
            for i in bridge.lans:
                for j in i.bridges:
                    j.message=j.message.compare(bridge.message)





class bridge:
    def __init__(self,name,lans,message):
        self.name=name
        self.lans=lans
        self.message=message
        self.adj=[]

    def display(self):
        lanslist=[]
        for lans in self.lans:
            lanslist.append(lans.name)
        adjlist=[x.name for x in self.adj]
        print('{}: {}: {}'.format(self.name, lanslist,adjlist))
        self.message.display()

class lan:
    def __init__(self,name,bridges):
        self.name=name
        self.bridges=bridges

    def display(self):
        bridgelist=[x.name for x in self.bridges]
        print('{}: {}'.format(self.name, bridgelist))

class message:
    def __init__(self,root,distance,sender):
        self.root=root
        self.distance=distance
        self.sender=sender

    def compare(self, message):
        if message.root<self.root:
            return message
        elif message.distance<self.distance:
            return message
        elif message.sender<self.sender:
            return message
        else:
            return self

    def display(self):
        print('({} {} {})'.format(self.root, self.distance, self.sender))





if __name__=='__main__':
    stpobj=stp(r"input\input1.txt")
    stpobj.initialize()
    for bridge in stpobj.BRIDGES:
        bridge.display()
    for lan in stpobj.LANS:
        lan.display()
    stpobj.sendMessages(0)
