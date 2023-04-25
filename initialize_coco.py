#!/usr/bin/env python
# coding: utf-8

#takes a directory with images and a text file with labels
#constructs the coco.json file without the annotations

import cv2
import json
import os

#directory with the images (ends with /)
photo_path = "./images/"
#file containing the labels (each in new line)
label_path = "./LabelsBiai.txt"
#description to add to the info tag
description = "BIAI 2023 Tomasz Michalik"

#the result file
output_path = "./result.coco.json"

#insert the info
coco = {}
coco["info"] = {}
coco["info"]["description"] = description

#insert the images
coco["images"] =[]
for name in os.listdir(photo_path):
    img = cv2.imread(photo_path + name)
    result = {}
    result["name"] = name
    result["width"] = img.shape[0]
    result["height"] = img.shape[1]
    
    coco["images"].append(result)


#initialize annotations
coco["annotations"] = []


#insert the labels
label_f = open(label_path)
coco["categories"]=[]
labels = label_f.read().split("\n")
label_f.close()
for i, v in enumerate(labels):
    label = {}
    label["id"] = i+1
    label["name"] = v
    coco["categories"].append(label)


#save the result
out = open(output_path, "w")
out.write(json.dumps(coco))
out.close()