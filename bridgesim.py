from bridge import Bridge, Lan, STP

if __name__=='__main__':
    stp=STP(r"input\input5.txt",r"output\output5.txt")
    stp.initialize()
    stp.generateSpanningTree()
    stp.writeOutput()
