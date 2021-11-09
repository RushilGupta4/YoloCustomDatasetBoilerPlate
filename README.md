# YoloCustomDatasetBoilerPlate_v4


This is a boilerplate for using yolo v4 with a custom dataset. <br/>
It will automatically install and configure yolo v4.

## Initialising Git Repository  
1) Clone the git repository using:
```
git clone https://github.com/Ruzil357/YoloCustomDatasetBoilerPlate_v4.git
```
2) Create a virtual environment using `requirements.txt`
<br/>

## Configuring The `config.json` File
1) Add the path to you nvcc in the `cuda_path` variable (can be found using `which nvcc`)
2) Choose your Yolo version
3) Choose you training split size

##Configuring Yolo Version Specific File
1) Find `model_config.json` in the directory `utils/your-yolo-version`
2) Add appropriate configurations in the file

## Using Custom Dataset
1) Under the `raw_data/images` folder, create a folder for each class
2) Add images for each class in their respective sub folders
3Run `create_dataset.py`

## Setting Up Yolo
To set up yolo, run yolo_setup.py with `src` as the working directory<br/>

## How To Train Yolo Using The Custom Dataset
1) Run `run.py` in the `src` directory and choose between training and testing