#COCO.json to .svg converter
#turns each annotation into separate .svg file
# result format: 
# filenameFromCoco.categoryID.sourceAnnotationID.svg


#requires svgwrite
#    pip install svgwrite 

#tested for python 3.10.10

import json
import os
import svgwrite

#the coco file 
inputPath = "./all.coco.json"
#directory to which output the resulting svg's, ends with a '/'
outputPath = "./coco_utils/"

#load the coco file
file = open(inputPath)
jsonfile = json.load(file)
file.close()

#make dictionary of images by their id
images = {}
for i in jsonfile["images"]:
    images[i["id"]] = i

    
for path in jsonfile["annotations"]:
    imgID = path["image_id"]
    
    #create a file
    filename = ".".join(images[imgID]["file_name"].split(".")[:-1]
        + [str(path["category_id"])]\
        + [str(path["id"])] + ["svg"])
    
    
    drawing = svgwrite.Drawing(outputPath + filename, size = (images[imgID]["width"], images[imgID]["height"] ))
    
    for segment in path["segmentation"]:
        p = svgwrite.path.Path()

        #path parameters
        p.attribs["fill"] = "none"
        p.attribs["stroke"] = "black"
        p.attribs["stroke-width"] = "1"
    
        #the path must start "M x,y" which defines the starting point
        #in this case it's the first vertex 
        p.push("M " + str(segment[0]) + ", "+str(segment[1]))

        #adding more vertices
        i = 0;
        while(i<len(segment)):
            p.push("L " +str(segment[i]) +"," + str(segment[i+1]))
            i += 2

        #close the path
        p.push("Z")
        drawing.add(p)
        
    #save the drawing
    drawing.save()