import matplotlib.pyplot as plt
import argparse
import sys
from os import listdir
from os.path import isfile, join

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-anchor_folder', default = "C:\\darknet\\scripts\\gen_anchors\\gen_anchors\\inc-vis", 
                        help='path to anchors directory\n', )
      
    args = parser.parse_args()

    anchor_files = [f for f in listdir(args.anchor_folder) if isfile(join(args.anchor_folder, f))]

    avg_IoUs = []
    indices = []

    for num_clusters in range(1,11):
        anchor_file = 'anchors%d.txt'%(num_clusters)
        
        try:
            f = open(join(args.anchor_folder,anchor_file))
        except IOError:
            print 'Could not open %s'%(anchor_file)
            exit(1)

            
        lines  = [line.rstrip('\n') for line in f.readlines()]

        indices.append(num_clusters)
        avg_IoUs.append(float(lines[1])) 

    plt.plot(indices,avg_IoUs,'o-')
    plt.ylabel('Mean Avg IOU')
    plt.xlabel('#clusters')
    plt.show()

if __name__ == '__main__':
    main(sys.argv)