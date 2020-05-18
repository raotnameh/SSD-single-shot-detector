# To reproduce the results please run the "run.sh" bash script present in the source_code folder. 

<!-- The implementation used is heavily based on the Max deGroot pytorch implementation: "https://github.com/amdegroot/ssd.pytorch". I would recommend to look at his repo also-->

#The total numner of bbox in the Ground truth are:: 2648.
#We report a 0.78 mAP on the given test set with the confidence threshold of 0.25 (we discard any object with a confidence less than 0.25, total numner of bbox in the prediction are:  3359). Furthermore, with a default confidence threshld of 0.01 we achieve 0.82 mAP but in this case total numner of bbox in the prediction are: 4403. Which means an increase of 1000 false positive bbox.

#The mAP score is almost same in both the cases but we are reducing around 1000 false positive bbox in the prediciton.


A. The dataset for this task is prepared in two steps:
	1. First downloading all the required files.
	2. Pre-process the data in the VOC format.
		2.1 annotated xml file is created " source_code/nidhi/VOC2007/Annotatinos"
		2.2 train and test split is created as given for the task. " source_code/nidhi/VOC2007/ImageSets/Main"
		2.3 All the images are put in one folder. " source_code/nidhi/VOC2007/JPEGImages"

B. Apart from the default data augmentation (normalizing the image, with mean and std), I did not use any augmented data to train the first draft.

C. Detection network used: In this implementation, I used SSD architecture as explained in the: "https://arxiv.org/pdf/1512.02325.pdf".
D. The default parameters are used in this study as used in the Max deGroot's implentation.
E. The number of classes is 2: one for the product and one for the backgorund class. 
F. For the anchor box: As mentioned in the task only 1 anchor box per feture map is allowed. we use 6 feture maps (38, 19, 10, 5, 3, 1) as mentioned in the paper. Additionally the number of default boxes are: 1940 because of the 1 anchor box used for each feature map. We use a fixed ratio (width ot height) for the anchor box used i.e.,"0.10, 0.12". The reason is explained in the next Section.



#Q&A

A. The purpose of using multiple anchors per feature map is to take into consideration/account the different shapes of object present in an image. For example, a car and human would need different anchor boxes shapes to correctly predict the bbox. 

B. This problem does not require multiple anchor boxes. Because, in the dataset all the products are of similar shape and one anchor box is all we need to take into consideration all the object shapes present in the dataset. Therfore, after the careful quantitaive analysis the average width to height ratio of "0.1/0.12" was found. And we use it for the width and height for each bbox in all the feature maps.


#This is the first draft and a considerable speed increase can be achieved for the particular dataset.
