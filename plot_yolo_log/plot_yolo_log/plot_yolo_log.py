import argparse 
import sys
import matplotlib.pyplot as plt

def main(argv):

    parser = argparse.ArgumentParser()


    parser.add_argument(
        "log_file",
        help = "path to log file"
        )

    parser.add_argument(
        "option",
        help = "0 -> loss vs iter"
        )
    
    args = parser.parse_args()

    f = open(args.log_file)
    
    lines  = [line.rstrip("\n") for line in f.readlines()]
    
    # skip the first 3 lines
    lines = lines[3:]
    
    numbers = {'1','2','3','4','5','6','7','8','9'}

    iters = []
    loss = []
    for line in lines:
        if line[0] in numbers and line[:2]!='1,':
            args = line.split(" ")
            iters.append(int(args[0][:-1]))
            loss.append(float(args[2]))             
    plt.plot(iters,loss)
    plt.xlabel('iters')
    plt.ylabel('loss')
    plt.grid()

    plt.show()
    
if __name__ == "__main__":
    main(sys.argv)