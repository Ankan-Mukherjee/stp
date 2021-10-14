from bridge import Bridge, Lan, STP

if __name__=='__main__':
    stp=STP()
    stp.initialize()
    stp.generateSpanningTree()
    stp.printOutput()
