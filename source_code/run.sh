#!/bin/bash

python data_prep.py

python -W ignore eval.py --voc_root nidhi/ --trained_model weights/VOC.pth

# Run this command to fine tune the model
#python -W ignore train.py --dataset_root nidhi/ --batch_size 32 --lr 0.000001 --resume weights/VOC.pth

python post_process.py

