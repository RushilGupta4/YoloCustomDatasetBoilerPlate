# YoloCustomDatasetBoilerPlate_v4


This is a boilerplate for using yolo v4 with a custom dataset. <br/>
It will automatically install and configure yolo v4.

## Initialising Git Repository  
1) Clone the git repository using:
```
git clone https://github.com/Ruzil357/YoloCustomDatasetBoilerPlate_v4.git
```
2Create a virtual environment using `requirements.txt`
<br/>

## Configuring The `config.json` File
1) Add the path to you nvcc in the `cuda_path` variable (can be found using `which nvcc`)
2) Choose configurations for your model (default configurations are already given)

## Using Custom Dataset
1) Under the `raw_data/images` folder, create a folder for each class
2) Add images for each class in their respective sub folders
3) Now open `create_dataset.py` and choose you testing size (default - 10%)
4) Run `create_dataset.py`

## Setting Up Yolo
To set up yolo v4, run yolo_setup.py with `src` as the working directory<br/>

## Switching Between Training And Testing Modes
To switch between modes, run `set_mode.py` ad choose between `train` or `test` <br/>

## How To Train Yolo Using The Custom Dataset
1) Set the model to training mode by running `set_mode.py`
2) Then run the following in the `src` directory: <br/>
`./darknet/dar detector train data/dataset.data cfg/yolov4-custom.cfg yolov4.conv.137 -dont_show -map`


## Steps
1) Clone git repository
2) Configure `config.json`
3) Add images to be labelled in `raw_images/images/{className}`
4) Run `create_dataset.py`
5) Run `yolo_setup.py`
6) Train model using the cmd:<br/>
`./darknet detector train data/dataset.data cfg/yolov4-custom.cfg yolov4.conv.137 -dont_show -map`