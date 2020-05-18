from map_boxes import mean_average_precision_for_boxes
import pandas as pd
from glob import glob
import numpy as np
from tqdm .auto import tqdm
from IPython.display import display as ipd
import IPython, os
import warnings
import pickle, json
warnings.filterwarnings("ignore")

#path to the predicted files on test set
results_path = 'nidhi/VOC2007/results/det_test_b.txt'
#confidence threshold
conf_threshold = 0.25

# predicted bbox and confidence score on the test set
with open(results_path, "r") as f:
    out = f.read()    
out = out.split('\n')[:-1]

# making a dict to plot an image an its all bbox
b = {}
pred = []
for i in tqdm(out):
    d = i.split(' ')
    if float(d[1]) > conf_threshold:
        pred.append(i)
        if d[0] in b.keys():
            b[d[0]].append(d[2:])
        else: 
            b[d[0]] = [d[2:]]


# To save the number of products for an image in the json format
save_image = {}
total_images = 0
for i in b.keys():
    img_name = i + '.jpg'
    save_image[img_name] = len(b[i])
    total_images+= len(b[i])
with open('../image2products.json', "w") as f:
    f.write(json.dumps(save_image, indent=4))


print("total numner of bbox in the prediction are: ", total_images)
print("total number of bbox in the Gtruth are 2648")


# Calcualting precision, recall and map.
a = 'ImageID,LabelName,Conf,XMin,YMin,XMax,YMax\n'
for i in pred:
    a+=i.split(' ')[0]+',0,'+','.join(i.split(' ')[1:]) + '\n'
with open('pred.csv', "w") as f:
    f.write(a)



with open('nidhi/VOC2007/annotations_cache/annots.pkl', "rb") as f:
    out = pickle.load(f)
    
a = 'ImageID,LabelName,XMin,YMin,XMax,YMax\n'
for i in out.keys():
    for j in out[i]:
        dummy = [str(i) for i in j['bbox']]
        a+=i+','+'0,'+','.join(dummy) + '\n'

with open('true.csv', "w") as f:
    f.write(a)
    
    
ann = pd.read_csv('true.csv')
det = pd.read_csv('pred.csv')
ann = ann[['ImageID', 'LabelName', 'XMin', 'XMax', 'YMin', 'YMax']].values
det = det[['ImageID', 'LabelName', 'Conf', 'XMin', 'XMax', 'YMin', 'YMax']].values
mean_ap, average_precisions, r, p = mean_average_precision_for_boxes(ann, det)

metrics = {
            'mAP': mean_ap,
            'precision': p,
            'recall': r[-1]  
            }

print(metrics)

with open('../metrics.json', "w") as f:
    f.write(json.dumps(metrics,indent=4))
