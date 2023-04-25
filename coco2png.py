#!/usr/bin/env python
# coding: utf-8

# generates masks from the input .coco.json file 
# result images are named as originals, just are png's


import cv2
import numpy as np
import os
from os.path import exists
import json

#function converting coco segment data into cv2 polygon data
#[x1, y1, x2, y2...] to [(x1,y1), (x2,y2)...]
def chunks(l):
    return [l[i:i+2] for i in range(0, len(l), 2)]



#the input file
inputPath = './result.coco.json' 
#directory to which output the masks (ends with '/')
outputDir = "./masks/" 

#read the file
f = open(inputPath)
coco = json.load(f)
f.close()


# colors to fill the masks for each category
colors = {4: (255,255,255),   #white
          3: (255,0,0),       #blue
          2: (0,255,0),       #greem
          1: (0,0,255)}       #red


# transform the coco file into more convenient data structure
# each image has its labels
# each label of an image has its annotations
images = {}
for im in coco["images"]:
    img = {}
    img["w"] = im["width"]
    img["h"] = im["height"]
    img["name"] = im["file_name"]
    img["anns"] = {}
    #prepare the labels container
    for i in range(1, len(coco["categories"])+1):
        img["anns"][i] = []
    
    #save to structure
    images[im["id"]] = img

#assign annotations to proper labels at proper images
#treats each segment as a separate annotation
for ann in coco["annotations"]:
    images[ann["image_id"]]["anns"] [ann["category_id"]].extend(ann["segmentation"])


# proper conversion -- for each image
for img_id, img_data in images.items():
    
    #create array the size of the image and fill it with black
    shape = (img_data["h"],img_data["w"],3)
    mask = np.ones(shape, dtype=np.uint8)
    mask.fill(0)
    
    #draw every segment of every label in the images
    for cat_id, cat_content in img_data["anns"].items():
        for segment in cat_content:
            points = chunks(segment)
            points = np.array(points, dtype=np.int32)
            cv2.fillPoly(mask, np.array([points]), colors[cat_id])
    
    #save the image
    cv2.imwrite(outputDir+".".join(img_data["name"].split(".")[:-1]+["png"]), mask)
 





