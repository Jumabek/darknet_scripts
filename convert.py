'''
Created on Mar 16, 2017

@author: jumabek
'''

from os import listdir
from os.path import isfile, join
import argparse
import cv2
import numpy as np
import sys
import os
import shutil
 
num_images = 0
size_w = 0
size_h = 0
def read_annotations(filename):
    f = open(filename,'r')
    annotations = []
    lines = [line.rstrip('\n')  for line in f.readlines()]
    for line in lines:
        (xmin,ymin,xmax,ymax) = map(float,line.split())

        bbox = (xmin,ymin,xmax,ymax)
        annotations.append(bbox)
    return annotations

def draw_annos(image,annos):
    for i in range(len(annos)):
        bbox_str = annos[i]
        bbox_int = [int(v) for v in bbox_str]
        [x,y,xmax,ymax] = bbox_int    
        xmin = min(x,xmax)
        ymin = min(y,ymax)
        xmax = max(x,xmax)
        ymax = max(y,ymax)


        cv2.rectangle(image,(x,y),(xmax,ymax),(0,0,255))


def write_clean_annos(filename, size, annos, filestream, image_file):
    global num_images,size_w,size_h 
    cls_id = 0 #since we onluy have one class
    if len(annos)==0:
        return
    
    num_images+=1
    size_w+=size[0]
    size_h+=size[1]

    f = open(filename,"w")
    filestream.write("%s \n"%image_file)        

    for i in range(len(annos)):
        
        bb = convert(size,annos[i])
        f.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    print "dw = {}, dh = {}".format(dw,dh)
    x = (box[0] + box[2])/2.0
    y = (box[1] + box[3])/2.0
    w = box[2] - box[0]
    h = box[3] - box[1]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

    
def process_video(images_dir,annos_dir,clean_annos_dir, fileliststream):
    
    
    print "images dir you provided {}".format(images_dir)
    print "annos dir you provided is {}".format(annos_dir)
    print "simple annos dir you provided is {}".format(clean_annos_dir)
    
    imagefiles = [f for f in listdir(images_dir) if isfile(join(images_dir, f))]
    
    annotations = [f for f in listdir(annos_dir) if isfile(join(annos_dir,f))]
    annotations = np.array(annotations)
    annotations = np.sort(annotations)
    
    #filtering '*.jpg' files
    imagefiles = [image_file for image_file in imagefiles if image_file[image_file.rfind('.')+1:]=='jpg' or image_file[image_file.rfind('.')+1:]=='png']
    imagefiles = np.array(imagefiles)
    imagefiles = np.sort(imagefiles)
    
    
    for i in range(imagefiles.shape[0]):
        image_file = join(images_dir,imagefiles[i])
        im = cv2.imread(join(images_dir,imagefiles[i]))
        annos = read_annotations(join(annos_dir,annotations[i]))

        if im is None or len(annos)<1:
            continue
        
    
        (h,w) = im.shape[:2]
        size = (w,h)
        write_clean_annos(join(clean_annos_dir, annotations[i]),size,annos,fileliststream,image_file)
        draw_annos(im,annos)
        cv2.imshow('image',im)
        cv2.waitKey(1000/12)


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def main(argv):
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-images_root', default = 'E:\\dataset\\fire_dataset\\Train\\images', # This dir name I cannot change cuz it will cause confusion 
                        help='path to root of the images dir\n', )
    
    parser.add_argument('-annos_root', default = 'E:\\dataset\\fire_dataset\\Train\\labels_original',  
                        help='path to root of the annotations dir ')
    
    parser.add_argument('-yolo_annos_root', default = 'E:\\dataset\\fire_dataset\\Train\\yolo_labels', 
                        help='path to root of simple annotations dir')

    parser.add_argument('-filelist', default = 'E:\\dataset\\fire_dataset\\Train\\filelist_train2.txt', 
                        help='name of the file where to save filelists')
    
    args = parser.parse_args()
    
    
    print "images_root you provided {}".format(args.images_root)
    print "annos_root you provided is {}".format(args.annos_root)
    print "yolo_annos_root you provided is {}".format(args.yolo_annos_root)
    
    groups = get_immediate_subdirectories(args.images_root)
    print groups

    #clean the directory that we want to generete annotations to
    
    shutil.rmtree(args.yolo_annos_root)

    fileliststream = open(args.filelist,'w')

    for group in groups:
        os.makedirs(join(args.yolo_annos_root,group))
        print "Passing %s"%('-images %s -annos %s -yolo_annos %s'%(join(args.images_root,group), join(args.annos_root,group), join(args.yolo_annos_root,group)))
        process_video(join(args.images_root,group), join(args.annos_root,group), join(args.yolo_annos_root,group),fileliststream)


    print "Number of images converted = {}".format(num_images)
    print "Average size = ({},{})".format(size_w/float(num_images),size_h/float(num_images))
if __name__=="__main__":
    main(sys.argv)
