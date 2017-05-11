# darknet_scripts
This repo contains my auxilary scripts to work with darknet deep learning famework

<h2>Is gen_anchors.py same as YOLOv2 anchor computation?</h2> 

<h2> Yes, almost. Look at the three anchors below:</h2>
<ul>
<li>
Original yolo-voc.2.0.cfg anchor is drawn in 416x416 blank image
<img src= 'https://github.com/Jumabek/darknet_scripts/blob/master/vizualize_anchors/vizualize_anchors/voc/yolo-voc.2.0.png'>
</li>

<br />
<li>
Original yolo-voc.cfg anchor is drawn in 416x416 blank image
<img src= 'https://github.com/Jumabek/darknet_scripts/blob/master/vizualize_anchors/vizualize_anchors/voc/yolo-voc.png'>
</li>
<br />

<li>
Computed bu gen_anchors.py yolo-voc-reproduce.cfg anchor is drawn in 416x416 blank image
<img src= 'https://github.com/Jumabek/darknet_scripts/blob/master/vizualize_anchors/vizualize_anchors/voc/anchors5.png'>
</li>

</ul>
