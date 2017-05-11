'''
Created on Feb 20, 2017

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
import random 

def IOU(x,centroids):
    dists = []
    k = len(centroids)
    for centroid in centroids:
        c_w,c_h = centroid
        w,h = x
        if c_w>=w and c_h>=h:
            dist = w*h/(c_w*c_h)
        elif c_w>=w and c_h<=h:
            dist = w*c_h/(w*h + (c_w-w)*c_h)
        elif c_w<=w and c_h>=h:
            dist = c_w*h/(w*h + c_w*(c_h-h))
        else: #means both w,h are bigger than c_w and c_h respectively
            dist = (c_w*c_h)/(w*h)
        dists.append(dist) # will become (k,) shape
    return np.array(dists) 

def avg_IOU(X,centroids):
    n,d = X.shape
    sum = 0.
    for i in range(X.shape[0]):
        #note IOU() will return array which contains IoU for each centroid and X[i] // slightly ineffective, but I am too lazy
        sum+= max(IOU(X[i],centroids)) 
    return sum/n

def write_anchors_to_file(centroids,X,anchor_file):
    f = open(anchor_file,'w')
    
    anchors = centroids*416/32
    
    print 'Anchors = ', centroids*416/32 
    
    num_anchors = anchors.shape[0]
    for i in range(num_anchors-1):
        f.write('%0.2f,%0.2f, '%(anchors[i][0],anchors[i][1]))

    #there should not be comma after last anchor, that's why
    f.write('%0.2f,%0.2f\n'%(anchors[num_anchors-1][0],anchors[num_anchors-1][1]))
    
    f.write('%f\n'%(avg_IOU(X,centroids)))

def kmeans(X,centroids,eps,anchor_file):
    
    N = X.shape[0]
    iterations = 0
    k,dim = centroids.shape
    prev_assignments = np.ones(N)*(-1)    

    while True:
        D = []            
        for i in range(N):
            D.append(1 - IOU(X[i],centroids))
        D = np.array(D) # D.shape = (N,k)
            
        #assign samples to centroids 
        assignments = np.argmin(D,axis=1)
        
        if (assignments == prev_assignments).all():
            print "Centroids = ",centroids            
            write_anchors_to_file(centroids,X,anchor_file)
            return

        #calculate the new centroids
        centroid_sums=np.zeros((k,dim),np.float)
        for i in range(N):
            centroid_sums[assignments[i]]+=X[i]
        
        for j in range(k):            
            centroids[j] = centroid_sums[j]/(np.sum(assignments==j)+0.0005)
        
        prev_assignments = assignments.copy()
        
def kmeans_noisy(X,centroids,eps,anchor_file):
    
    D=[]
    old_D = []
    iterations = 0
    diff = 1e5
    c,dim = centroids.shape

    while True:
        iterations+=1
        D = []            
        for i in range(X.shape[0]):
            d = 1 - IOU(X[i],centroids)
            D.append(d)
        D = np.array(D) # D.shape = (N,k)
        if len(old_D)>0:
            diff = np.sum(np.abs(D-old_D))
        
        print 'diff = %f'%diff

        if diff<eps or iterations>100:
            print "Number of iterations took = %d"%(iterations)
            print "Centroids = ",centroids

            
            write_anchors_to_file(centroids,X,anchor_file)
            
            return

        #assign samples to centroids 
        belonging_centroids = np.argmin(D,axis=1)
        print belonging_centroids 

        #calculate the new centroids
        centroid_sums=np.zeros((c,dim),np.float)
        for i in range(belonging_centroids.shape[0]):
            centroid_sums[belonging_centroids[i]]+=X[i]
        
        for j in range(c):
            
            print '#annotations in centroid[%d] is %d'%(j,np.sum(belonging_centroids==j))
            centroids[j] = centroid_sums[j]/np.sum(belonging_centroids==j)
        
        print 'new centroids = ',centroids        



        old_D = D.copy()
    print D


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-filelist', default = 'E:\\dataset\\face_detection\\WIDER\\filelist_all.txt', 
                        help='path to filelist\n' )
    parser.add_argument('-num_clusters', default = 0, type = int, 
                        help='number of clusters\n' )  
    parser.add_argument('-output_dir', default = 'anchors', type = str, 
                        help='Output anchor directory\n' )  

   
    args = parser.parse_args()
    

    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)


    f = open(args.filelist)
    

    lines = [line.rstrip('\n') for line in f.readlines()]
    
    annotation_dims = []
    for line in lines:
        
        line = line.replace('images','labels')
        line = line.replace('img1','labels')
        line = line.replace('JPEGImages','labels')        

        line = line.replace('.jpg','.txt')

        f2 = open(line)
        for line in f2.readlines():
            line = line.rstrip('\n')
            cls_id = line.split(' ')[0]

            cls_id = int(cls_id)
            if cls_id!=0:
                continue
            w,h = line.split(' ')[3:]
            #print w,h
            annotation_dims.append(map(float,(w,h)))
    annotation_dims = np.array(annotation_dims)
    
    
    eps = 0.005
    
    if args.num_clusters == 0:
        for num_clusters in range(1,11): #we make 1 through 10 clusters 
            anchor_file = join( args.output_dir,'anchors%d.txt'%(num_clusters))

            indices = [ random.randrange(annotation_dims.shape[0]) for i in range(num_clusters)]
            centroids = annotation_dims[indices]
            kmeans(annotation_dims,centroids,eps,anchor_file)
            print 'centroids.shape', centroids.shape
        print 'Filelist = %s'%(args.filelist)
    else:
        anchor_file = join( args.output_dir,'anchors%d.txt'%(args.num_clusters))
        indices = [ random.randrange(annotation_dims.shape[0]) for i in range(args.num_clusters)]
        centroids = annotation_dims[indices]
        kmeans(annotation_dims,centroids,eps,anchor_file)


        print 'centroids.shape', centroids.shape
        print 'Filelist = %s'%(args.filelist)

if __name__=="__main__":
    main(sys.argv)
