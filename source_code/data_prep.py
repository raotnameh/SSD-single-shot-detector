from glob import glob
import numpy as np
from tqdm .auto import tqdm
import warnings, os
import matplotlib.pyplot as plt
from PIL import Image
warnings.filterwarnings("ignore")

def rea(d):
    with open(d,"r") as f:
        return f.read()


os.system(f"mkdir nidhi/")
os.system(f"mkdir nidhi/VOC2007")
os.system(f"mkdir nidhi/VOC2007/Annotations")
os.system(f"mkdir nidhi/VOC2007/JPEGImages")
os.system(f"mkdir nidhi/VOC2007/ImageSets")
os.system(f"mkdir nidhi/VOC2007/ImageSets/Main")

os.system(f"git clone https://github.com/gulvarol/grocerydataset.git")
os.system(f"wget https://storage.googleapis.com/open_source_datasets/ShelfImages.tar.gz")
os.system(f"tar -xvf ShelfImages.tar.gz")
os.system(f"mv ShelfImages/ grocerydataset/")
os.system(f"mv grocerydataset/ nidhi/")
os.system(f"rm ShelfImages.tar.gz ")


# path to the annotation .csv file
path = 'nidhi/grocerydataset/annotations.csv'
# path to save all the .xml files
annot_save = 'nidhi/VOC2007/Annotations/'
# path to save all the images to train and test
image_save = 'nidhi/VOC2007/JPEGImages/'
# path to train and test splits.
split_save = 'nidhi/VOC2007/ImageSets/Main/'
# path to the training image folder
train_ = 'nidhi/grocerydataset/ShelfImages/train/'
# path to the testing image flder
test_= 'nidhi/grocerydataset/ShelfImages/test/'





annotations = rea(path).split('\n')


data = {}
for i in tqdm(annotations):
    d = i.split(',')
    if not d[0]:
        continue
    try:w,h = Image.open(train_+d[0]).size
    except: w,h = Image.open(test_+d[0]).size
    if d[0] in data.keys():
        data[d[0]].append(d[1:]+[h,w])
    else: 
        data[d[0]] = [d[1:] + [h,w]]


import pandas as pd
from lxml import etree
import xml.etree.cElementTree as ET

# To pretty indent the .xml file
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


# Creating the .xml files for all the data
for k,v in tqdm(data.items()):
    height = v[0][-2]
    width = v[0][-1]
    depth = 3
    annotation = ET.Element('annotation')
    ET.SubElement(annotation, 'folder').text = 'images'
    ET.SubElement(annotation, 'filename').text = str(k)
    size = ET.SubElement(annotation, 'size')
    ET.SubElement(size, 'width').text = str(width)
    ET.SubElement(size, 'height').text = str(height)
    ET.SubElement(size, 'depth').text = str(depth)
    ET.SubElement(annotation, 'segmented').text = '0'

    for j in v:
        ob = ET.SubElement(annotation, 'object')
        ET.SubElement(ob, 'name').text = "b" # str(j[4]) class of the bbox
        ET.SubElement(ob, 'pose').text = 'Unspecified'
        ET.SubElement(ob, 'truncated').text = '0'
        ET.SubElement(ob, 'difficult').text = '0'
        bbox = ET.SubElement(ob, 'bndbox')
        ET.SubElement(bbox, 'xmin').text = str(j[0])
        ET.SubElement(bbox, 'ymin').text = str(j[1])
        ET.SubElement(bbox, 'xmax').text = str(j[2])
        ET.SubElement(bbox, 'ymax').text = str(j[3])
    
    fileName = str(k.split('.')[0])
    tree = ET.ElementTree(annotation)
    indent(annotation)
    tree.write(annot_save+fileName + ".xml", encoding='utf8')


#creating train and test files
im = os.listdir(train_)
a = ''
for i in im:
    a+= os.path.basename(i).split('.')[0] + '\n'
with open(split_save+'trainval.txt', "w") as f:
    f.write(a)


im = os.listdir(test_)
a = ''
for i in im:
    a+= os.path.basename(i).split('.')[0] + '\n'
with open(split_save+'test.txt', "w") as f:
    f.write(a)

#combine the train and test images in one folder
os.system(f"cp {train_}* {image_save}")
os.system(f"cp {test_}* {image_save}")

for i in glob(f"{image_save}*.JPG"):
    os.system(f"cp {i} {i.split('.')[0]+'.jpg'}")
os.system(f"rm {image_save}*.JPG")

os.system(f'rm -rf nidhi/grocerydataset/')

os.system(f"mkdir weights")
os.system(f"wget wget https://s3.amazonaws.com/amdegroot-models/vgg16_reducedfc.pth")
os.system(f"mv vgg16_reducedfc.pth weights/")