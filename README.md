# darknet_scripts
This repo contains my auxilary scripts to work with darknet deep learning famework
1. [How to reproduce YOLOv2 anchors for yolo-voc.cfg?](#how-to-use)
2. [How to visualize genereted anchors?](#how-to-compile)
3. [Is gen_anchors.py same as YOLOv2 anchor computation](#how-to-train-pascal-voc-data)
4. [How to plot YOLO loss](#how-to-train-to-detect-your-custom-objects)
5. [When should I stop training](#when-should-i-stop-training)
6. [How to improve object detection](#how-to-improve-object-detection)
7. [How to mark bounded boxes of objects and create annotation files](#how-to-mark-bounded-boxes-of-objects-and-create-annotation-files)
8. [How to use Yolo as DLL](#how-to-use-yolo-as-dll)

### How to reproduce YOLOv2 anchors for yolo-voc.cfg?
<h2>How to reproduce YOLOv2 anchors for yolo-voc.cfg?</h2>
follow the below steps 2-5(cut from AlexeyAB's repos)

2. Download The Pascal VOC Data and unpack it to directory `build\darknet\x64\data\voc` will be created dir `build\darknet\x64\data\voc\VOCdevkit\`:
    * http://pjreddie.com/media/files/VOCtrainval_11-May-2012.tar
    * http://pjreddie.com/media/files/VOCtrainval_06-Nov-2007.tar
    * http://pjreddie.com/media/files/VOCtest_06-Nov-2007.tar
    
    2.1 Download file `voc_label.py` to dir `build\darknet\x64\data\voc`: http://pjreddie.com/media/files/voc_label.py

3. Download and install Python for Windows: https://www.python.org/ftp/python/3.5.2/python-3.5.2-amd64.exe

4. Run command: `python build\darknet\x64\data\voc\voc_label.py` (to generate files: 2007_test.txt, 2007_train.txt, 2007_val.txt, 2012_train.txt, 2012_val.txt)

5. Run command: `type 2007_train.txt 2007_val.txt 2012_*.txt > train.txt`

Next, call <br/> 
<strong>
python gen_anchors.py -filelist //path//to//voc//filelist/list//train.txt -output_dir generated_anchors/voc-reproduce -num_clusters 5
</strong>
<br />
You will have anchors5.txt in generated_anchors/voc-reproduce folder. <br />

<h2>How to visualize genereted anchors?</h2>
After completing the steps above, execute <br />
<strong> python visualize_anchors.py -anchor_dir generated_anchors/voc-reproduce </strong>
<br />
Inside the generated_anchors/voc-reproduce directory you will have png visualization of the anchors <br />



<h2>Is gen_anchors.py same as YOLOv2 anchor computation?</h2> 

<h4> Yes, almost. Look at the two anchors below:</h4>
<br />
<ul>

<li>
yolo-voc.cfg anchors are provided by the original author
<img src= 'https://github.com/Jumabek/darknet_scripts/blob/master/generated_anchors/voc-original/yolo-voc.png' />
</li>
<br />

<li>
yolo-voc-reproduce.cfg anchors computed by gen_anchors.py 
<img src= 'https://github.com/Jumabek/darknet_scripts/blob/master/generated_anchors/voc-anchors-reproduce/anchors5.png' />
</li>
<br />
</ul>



<h2>How to get anchors if My input for network is bigger than 416?</h2>
Simply change the lines here https://github.com/Jumabek/darknet_scripts/blob/master/gen_anchors.py#L17
to your input dimension.
Then compute the anchors.



<h2>How to plot YOLO loss?</h2>
In order to plot a loss, you first need a log of the <i>darknet train</i> command
For example,below command will save the log into log/aggregate-voc-tiny7.log <br /><br />
<i>
darknet.exe detector train data/aggregate-voc-tiny7.data cfg/aggregate-voc-tiny7.cfg  backup/aggregate-voc-tiny7/aggregate-voc-tiny7_21000.weights >> log/aggregate-voc-tiny7.log -gpus 0,1
</i>
<br />
<br />
Next, to plot the loss, execute <br/>
<i>python plot_yolo_log.py \\path\\to\\log\\aggregate-voc-tiny7.log</i>
