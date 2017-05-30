<h4>How to generate YOLOv2 anchors?</h4>
type in the command line <br />
<strong>gen_anchors.py -filelist   \\path\\to\\voc-filelist\\filelist.txt   -num_clusters  5   -output_dir voc-anchors </strong>
</br>
Filelist is the text file that contains path to images in your database.
Here is an instruction on how to prepare filelist (train.txt) for VOC (sections 2 through 5) https://github.com/AlexeyAB/darknet#how-to-train-pascal-voc-data
<br/>
This is a sample of how my train.txt filelist looks like:
<br/>
<i>
C:\darknet\build\darknet\x64\data\voc/VOCdevkit/VOC2007/JPEGImages/000012.jpg
C:\darknet\build\darknet\x64\data\voc/VOCdevkit/VOC2007/JPEGImages/000017.jpg
C:\darknet\build\darknet\x64\data\voc/VOCdevkit/VOC2007/JPEGImages/000023.jpg
C:\darknet\build\darknet\x64\data\voc/VOCdevkit/VOC2007/JPEGImages/000026.jpg
C:\darknet\build\darknet\x64\data\voc/VOCdevkit/VOC2007/JPEGImages/000032.jpg
C:\darknet\build\darknet\x64\data\voc/VOCdevkit/VOC2007/JPEGImages/000033.jpg
C:\darknet\build\darknet\x64\data\voc/VOCdevkit/VOC2007/JPEGImages/000034.jpg
</i>

<br />

gen_anchors.py reads yolo format annotations from filelist (train.txt)
when you run the following command, you should get voc-anchors folder which contain number of anchors from 1 to 10.  
<strong>python gen_anchors.py -filelist
C:\darknet\build\darknet\x64\data\voc\train.txt -output_dir voc-anchors </strong> 


<h4>How to visualize anchors?</h4>
type in the command line <br />
<strong>python vizualize_anchors.py -anchor_dir F:\code\darknet_scripts\gen_anchors\gen_anchors\voc-anchors </strong>
and you will get png images inside -anchor_dir



