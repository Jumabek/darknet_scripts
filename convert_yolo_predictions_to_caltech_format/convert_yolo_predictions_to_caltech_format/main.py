from os import listdir
from os.path import isfile, join
import argparse
import cv2
import numpy as np
import sys
import os
import shutil
      

def save_file_predictions(root,predictions,stream):
    for prediction in predictions:
        (confidence,xmin,ymin,xmax,ymax) = map(float,prediction.split(' ')[1:]) #leaving out [0] because it corresponds to ID
        w = xmax - xmin
        h = ymax - ymin
        
        stream.write('%f %f %f %f %f \n'%(xmin,ymin,w,h,confidence)) 

def open_file(root,id):
   
    set_folder_name,video_folder_name,image_file_name =  id.split('\\')[-3:]

    #print 'image_file_name = %s'%(image_file_name)
    #print 'video_folder_name = %s'%(video_folder_name)
    #print 'set_folder_name = %s'%(set_folder_name) 
    
    video_dir = join(root,set_folder_name,video_folder_name)
    
    if not os.path.isdir(video_dir):
        os.makedirs(video_dir)    
    f = open(join(video_dir,image_file_name+'.txt'),'w')
    print join(video_dir,image_file_name+'.txt')
    return f

     
def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-predictions_file', default = 'C:\\darknet\\build\\darknet\\x64\\results\\comp4_det_test_person.txt', # This dir name I cannot change cuz it will cause confusion 
                        help='path to yolo predictions\n', )
    
    parser.add_argument('-caltech_pedestrian_root', default = 'E:\\dataset\\CaltechPedestrians\\code\\data-USA\\res\\caltech-161K-vis-original2x',  
                        help='where to save converted predictions')
        
    args = parser.parse_args()
    
    
    print "predictions_file you provided {}".format(args.predictions_file )
    print "caltech_pedestrian_root you provided is {}".format(args.caltech_pedestrian_root)
    
    if not os.path.exists(args.caltech_pedestrian_root):
        os.mkdir(args.caltech_pedestrian_root)
        

    f = open(args.predictions_file)
    lines = [line.rstrip('\n') for line in f.readlines()]
    
    subdirs = os.listdir(args.caltech_pedestrian_root)
    if len(subdirs) >5:
        print '%s is non empty please specify empty dir'%(args.caltech_pedestrian_root)
        print subdirs
        return
    else:
        print '%s is empty ;). Continuing'%(args.caltech_pedestrian_root)


    single_file_predictions = []
    
    id = lines[0].split()[0]
    f = open_file(args.caltech_pedestrian_root, id)
    

    for line in lines:
        if line.split()[0] !=id:
            
            save_file_predictions(args.caltech_pedestrian_root,single_file_predictions,f)

            #start new file
            id = line.split(' ')[0]
            f = open_file(args.caltech_pedestrian_root, id) # if already created, then do nothing
            single_file_predictions = []
        
        single_file_predictions.append(line)
        



if __name__=="__main__":
    main(sys.argv)
