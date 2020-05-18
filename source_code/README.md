<!-- #Run the "run.sh" bash script to do all the steps -->

#Use cuda 10.1 for this implentation
#Create and activate the conda environment before running the "run.sh" bash script
"conda env create -f environment.yml"
"conda activate ssd"

#Data preparation step: 1. Download and pre-process the data required for training and testing
data_prep_command: "python data_prep.py"

#Training command, if do not want to fine-tune the model remove the --resume argument.
train_command = "python -W ignore train.py --dataset_root nidhi/ --batch_size 32 --lr 0.000001 --resume weights/VOC.pth"

#Evaluatino script to save the predicted bbox's
eval_command: "python -W ignore eval.py --voc_root nidhi/ --trained_model weights/VOC.pth"

#Post processig step to caclulate the mAp, precision, and recall. Also it saves the number of products in each image.
post_process_command: "python post_process.py"


#Confidence threshold probability used during the prediction step.
confidence_threshold = "0.25"
