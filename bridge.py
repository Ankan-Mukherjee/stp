import copy

class Stp:
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
            lans=[x.rstrip() for x in line.split(':')[1] if x.isalpha()]
            mess=Message(name,0,name)
            self.BRIDGES.append(Bridge(name,lans,mess))

    def fillLans(self):
        lannames=[]
        for bridge in self.BRIDGES:
            for lans in bridge.lans:
                if lans not in lannames:
                    lannames.append(lans)
                    self.LANS.append(Lan(lans,[]))
        for lans in self.LANS:
            for bridge in self.BRIDGES:
                if lans.name in bridge.lans:
                    lans.bridges.append(bridge.name)

    def initialize(self):
        self.BRIDGES=[]
        self.LANS=[]
        self.readInput()
        self.fillLans()
        for bridge in self.BRIDGES:
            for lan in self.LANS:
                if lan.name in bridge.lans:
                    for bridge_inner in self.BRIDGES:
                        if bridge_inner.name in lan.bridges and bridge_inner.name!=bridge.name and bridge_inner.name not in bridge.adj:
                            bridge.adj.append(bridge_inner.name)

            #print()


    def displayMessage(self,time,type,node,message):
        print('{} {} {}'.format(time,type,node.name),end=' ')
        message.display()

    def sendMessages(self, time):
        for bridge in self.BRIDGES:
            message_temp=copy.deepcopy(bridge.message)
            message_temp.sender=bridge.name
            for i in bridge.lans:
                self.displayMessage(time,'s',bridge,message_temp)
            for i in bridge.adj:
                for j in self.BRIDGES:
                    if j.name==i:
                        j.received.append(message_temp)

    def receiveMessages(self, time):
        for bridge in self.BRIDGES:
            for i in bridge.received:
                self.displayMessage(time,'r',bridge,i)
                        #bridge.received.append(bridge_inner.message)

    def updateMessages(self):
        flag=False
        for bridge in self.BRIDGES:
            for received in bridge.received:
                #received.display()
                received_copy=copy.deepcopy(received)
                received_copy.distance+=1
                message_temp=bridge.message.compare(received_copy)
                flag=flag or bridge.message.compareBool(message_temp)
                bridge.message=message_temp
                #bridge.message.display()
            #print()
            bridge.received=[]
        return flag

    def establishConnection(self):
        time=0
        flag=True
        while True:
            self.sendMessages(time)
            self.receiveMessages(time+1)
            flag=self.updateMessages()
            if flag == False:
                break
            time+=1

class Bridge:
    def __init__(self,name,lans,message):
        self.name=name
        self.lans=lans
        self.message=message
        self.adj=[]
        self.received=[]

    def display(self):
        print('{}: {}: {}'.format(self.name, self.lans, self.adj))
        self.message.display()

class Lan:
    def __init__(self,name,bridges):
        self.name=name
        self.bridges=bridges

    def display(self):
        print('{}: {}'.format(self.name, self.bridges))

class Message:
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

    def compareBool(self, message):
        if message.root<self.root:
            return True
        elif message.distance<self.distance:
            return True
        elif message.sender<self.sender:
            return True
        else:
            return False


    def display(self):
        print('({} {} {})'.format(self.root, self.distance, self.sender))

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
    stpobj=Stp(r"input\input1.txt")
    stpobj.initialize()
    for bridge in stpobj.BRIDGES:
        bridge.display()
    for lan in stpobj.LANS:
            lan.display()
    stpobj.establishConnection()
    for bridge in stpobj.BRIDGES:
            bridge.display()
