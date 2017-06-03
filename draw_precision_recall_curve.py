import sys
import argparse
import matplotlib.pyplot as plt
from pylab import *
import numpy as np

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file',default = "C:\\darknet_fire_detection\\build\\darknet\\x64\\log\\precision_recall5.txt", help="file to read precision and recall")
    #parser.add_argument('-output_file',default = "C:\\darknet_fire_detection\\build\\darknet\\x64\\log\\precision_recall3.png", help='full path to save curve')

    args = parser.parse_args()
    args.output_file = args.input_file.replace(".txt",".png")

    print "input file you provided is {}".format(args.input_file)

    print "output file you provided is {}".format(args.output_file)
    f = open(args.input_file)    

    lines = [line.rstrip("\n") for line in f.readlines()]

    iters = []
    precisions = []
    recalls = []
    
    for line in lines:
        cols = line.split()
        if len(cols)<3:
            continue
        iters.append(float(cols[0][:-1]))
        precisions.append(float(cols[1]))
        recalls.append(float(cols[2]))

    print iters
    print precisions
    print recalls

    fig= plt.figure()
    ax = fig.add_subplot(111)
    #figure()
    #gca().set_position((.1, .3, .8, .6))
    plt.plot(iters,precisions,label = "precision")
    plt.plot(iters,recalls, label = "recall")
    plt.legend()
    ax.set_yticks(np.linspace(0,1,11))
    plt.grid()
    plt.xlabel("number of iterations in K(1.0 means 1000)")
    plt.ylabel("precision/recall value. Ideally should be 1")    
    #plt.figtext(0.95,0.9, "High recall means detect most of the fires cases. \n Low precision means a lot of misalarm")
    savefig(args.output_file)
    plt.show()













if __name__ == "__main__":
    main(sys.argv)