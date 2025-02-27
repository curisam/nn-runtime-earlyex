# nn-runtime-earlyex

A tool for Neural Network to achieve early exit results with metric learning based classifiers
Backbone Training is highly recommended.

## 1. Training Backbone
1. set configure file backbone.yml
2. run the following code to train backbone model:
```
python train_backbone.py --config ./configs/backbone.yml
```
3. run the following code to test backbone model:
```
python test_backbone.py --config ./configs/backbone.yml
```

## 2a. Adding & Training (Cross Entropy) Branch With Calibration
1. set configure file ce_branch.yml
2. run the following code to train model:
```
python train_ce_branch.py --config ./configs/ce_branch.yml
```
3. run the following code to test model:
```
python test_ce_branch.py --config ./configs/ce_branch.yml
```
## 2b. Adding & Training (Metric) Branch with Calibration
1. set configure file metric.yml
2. run the following code to train model:
```
python train_me_branch.py --config ./configs/me_branch.yml
```
3. run the following code to test model:
```
python test_me_branch.py --config ./configs/me_branch.yml
```

# Improved Early Exiting Activation to Accelerate Edge Inference

## Overall Architecture

<img width="282" alt="arch" src="https://user-images.githubusercontent.com/12655218/125258223-19c64f80-e339-11eb-9767-c46a1a507ecf.PNG">

## Adding Early Exiting exceptions to Non-linear Activations
<img width="462" alt="EarlyExit_1" src="https://user-images.githubusercontent.com/12655218/125258674-880b1200-e339-11eb-8f10-07fc36c5a764.PNG">

## Selecting Early Exiting Branches based on Cross Entropy Validation Loss
<img width="462" alt="val_loss" src="https://user-images.githubusercontent.com/12655218/125258547-6c077080-e339-11eb-9a97-925ce4ebbfa7.PNG">

## Experiments results
<img width="454" alt="table0" src="https://user-images.githubusercontent.com/12655218/125258818-aa049480-e339-11eb-9595-2035c9b03d40.PNG">
<img width="370" alt="table1" src="https://user-images.githubusercontent.com/12655218/125258822-aa9d2b00-e339-11eb-9ede-226c186ff05d.PNG">

We perform experiments on ResNet-18 and ResNet-34

## Requirements:
The following are required to run this program:
```
dataclasses
numpy
pandas
pyyaml
tqdm
Pytorch>=1.7.0
torchvision>=0.8.1

```

## Usage:
```
usage: main.py [-h] [--pretrained PRETRAINED] [--best BEST]
               [--backbone BACKBONE] [--dataset DATASET] [--dali DALI]
               [--data_dir DATA_DIR] [--epoch EPOCH] [--device DEVICE]
               [--num_class NUM_CLASS] [--batch_size BATCH_SIZE]
               [--workers WORKERS] [--img_size SIZE] [--lr LR] 
```

### Acknowledgement
This work was supported by Institute of Information & communications Technology Planning & Evaluation (IITP) grant funded by the Korea government(MSIT) (No. 2021-0-00907, Development of Adaptive and Lightweight Edge-Collaborative Analysis Technology for Enabling Proactively Immediate Response and Rapid Learning).
