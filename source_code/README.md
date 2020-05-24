## **Use cuda 10.1**
### To create and activate the conda environment.
  * conda env create -f environment.yml
  * conda activate ssd

*Run the "run.sh" bash script to do all the steps (bash run.sh).*

### Data preparation step. 
  *Download and pre-process the data required for training and testing:
    * python data_prep.py

### Training command, if do not want to fine-tune the model remove the --resume argument.
  * python -W ignore train.py --dataset_root nidhi/ --batch_size 32 --lr 0.000001 --resume weights/VOC.pth

### Evaluatino script to save the predicted bbox's
* python -W ignore eval.py --voc_root nidhi/ --trained_model weights/VOC.pth

### Post processig step to caclulate the mAp, precision, and recall. Also it saves the number of products in each image.
* python post_process.py"


##### Confidence threshold probability used during the prediction step: *0.25*
