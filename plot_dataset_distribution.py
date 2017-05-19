import argparse 
import sys
import matplotlib.pyplot as plt
import re

def main(argv):

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "log_file",
        help = "Log file"
        )

    parser.add_argument(
        "begin_iter", type=int,
        help = "begin iteration of the selction"
        )
    parser.add_argument(
        "end_iter",type=int,
        help = "end of iteration"
        )
    parser.add_argument(
        "width",type=int,
        help = "length of interval"
        )

    args = parser.parse_args()

    f = open(args.log_file)
    
    lines  = [line.rstrip("\n") for line in f.readlines()]
    
    numbers = {'1','2','3','4','5','6','7','8','9'}
    
    
    fig,ax = plt.subplots()   
    
    width = args.width
    num_partitions = int((args.end_iter - args.begin_iter + 0.9)/width )
    num_partitions+=1 # this is for dataset_ratio
    partition=1

    plt.subplot(num_partitions,2,partition)

    dataset_ratio = {'caltech-pedestrian':14302,
'ETH':3429,
'INRIAPerson':900,
'MOT17Det':5316,
'tud-brussels-motionpairs':507,
'tud-crossing-sequence':200,
'voc_person':6095}
    
    plt.bar(xrange(1,8),dataset_ratio.values(),color='g')
    ax.set_title('Dataset ratio')
    

    for begin in range(args.begin_iter,args.end_iter,width):
        partition+=1
        end = begin+width
        filenames = []
        dataset_names = []

        dataset_counts = {'caltech-pedestrian':0,'ETH':0,'INRIAPerson':0,
                    'MOT17Det':0,'tud-brussels-motionpairs':0,
                    'tud-crossing-sequence':0,'voc_person':0}
        iter = 0
        for line in lines:
            vars = line.split(' ')

            if vars[0][-1:]==':' and vars[0][0] in numbers :
                iter = int(vars[0][:-1])            
            if iter>end:
                break        

            if iter>begin and iter<end:
                
                if line.startswith('grp:'):
                    filename = line.split(' ')[1]
                    filenames.append(filename)
                    
                    dataset_args = filename.split('\\')
                    #print dataset_args 
                    dataset_names.append(dataset_args[3])          
                    dataset_counts[dataset_args[3]]+=1
        print 'len of the images  = ',len(dataset_names)
        print dataset_counts
        
        
        plt.subplot(num_partitions,2,partition)
        print dataset_counts.keys()
        print dataset_counts.values()
        plt.bar(xrange(1,8),dataset_counts.values())
        print 
    plt.show()
    
  
    
if __name__ == "__main__":
    main(sys.argv)