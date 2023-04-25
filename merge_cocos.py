#!/usr/bin/env python
# coding: utf-8

#merges many .coco.json files into one 
#makes sure all IDs stay unique
#assumes all images have the same categories

import os
import json

#directory containing the .coco.json files (ends with '/')
imagesDir = "./coco/"

#result file 
resultFilename = "./result.coco.json"

#initialize result
final_coco = {}

#take the constant attributes from the first file

#get the file
first_coco_name =  os.listdir(imagesDir)[0]
first_coco_file = open(imagesDir+first_coco_name, encoding="utf-8")
first_coco = json.load(first_coco_file)
first_coco_file.close()

#copy its attributes
final_coco = first_coco

#remove annotations and images
final_coco["annotations"] = []
final_coco["images"] = []

current_im_id = 1
current_ann_id = 1

for f in os.listdir(imagesDir):
    #open coco file
    file = open(imagesDir+f, encoding="utf-8")
    coco = json.load(file)
    file.close()
    
    #change the image id
    translate_id = {}
    
    for im in coco["images"]:
        translate_id[im["id"]] = current_im_id
        im["id"] = current_im_id
        final_coco["images"].append(im)
        current_im_id += 1
    
    #add annotation to result
    #first change annotation id 
    for ann in coco["annotations"]:
        ann["image_id"] = translate_id[ann["image_id"]]
        ann["id"] = current_ann_id
        current_ann_id += 1
        final_coco["annotations"].append(ann)
    
    
#save result to file
file = open(resultFilename, "w")
file.write(json.dumps(final_coco))
file.close()
