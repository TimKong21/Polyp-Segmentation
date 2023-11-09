# Polyp Segmentation

## **Introduction**

This project aims to perform polyp segmentation in endoscopy images using the U-Net architecture. The model is trained on the Kvasir-SEG dataset and aims to provide accurate and efficient segmentation to assist in medical diagnosis.

## **Dataset**

The model is trained on the Kvasir-SEG dataset, which is a collection of endoscopy images specifically designed for polyp segmentation tasks. The dataset is hosted by Simula Research Laboratory, the website to the dataset can be accessed [here](https://datasets.simula.no/kvasir-seg/). 

For more information, refer to the publication: **[Kvasir-SEG: A Segmented Polyp Dataset](https://arxiv.org/pdf/1911.07069.pdf)**

## Installation

To get started, please follow steps below:

1. Download all the project assets from the provided [Google Drive link](https://drive.google.com/drive/folders/1rxoyNXTvHEPsNYPfMxLFqPmNjBByp5oA?usp=sharing) to your respected directory.
2. Unzip the folder in the same directory.
3. In your favorite command line interface, change current directory to the respected directory.
4.  Install the required packages with command below. 

```bash
pip install -r requirements.txt
```

## Project assets description

There are two IPython Notebooks (with `.ipynb` extension):

1. *EDA and Dataset Preperation.ipynb*
2. *Image preprocessing Data generator and Modeling.ipynb*

### *EDA and Dataset Preperation.ipynb*

When the *Kvasir-SEG* folder is unzipped, the file names are not readable and serialized. 
For example:

```markdown
Kvasir-SEG
├── images
│   ├── cju0qkwl35piu0993l0dewei2.jpg
│   ├── cju0qoxqj9q6s0835b43399p4.jpg
│   ├── ...
│   
├── masks
│   ├── cju0qkwl35piu0993l0dewei2.jpg
│   ├── cju0qoxqj9q6s0835b43399p4.jpg
│   ├── ...
│
└── kavsir_bboxes.json
```

This notebook will rename and serialize the files, then split them into train, validation, and test set in a new folder named *new_data*. For example:

```markdown
new_data
├── test
│   ├── images
│       ├── 0011.jpg
|       ├── 0024.jpg
|       ├── ...
│   ├── masks
│       ├── 0011.jpg
|       ├── 0024.jpg
|       ├── ...
|
├── train
│   ├── images
│       ├── 0001.jpg
|       ├── 0002.jpg
|       ├── ...
│   ├── masks
│       ├── 0001.jpg
|       ├── 0002.jpg
|       ├── ...
|
├── valid
│   ├── images
│       ├── 0008.jpg
|       ├── 0009.jpg
|       ├── ...
│   ├── masks
│       ├── 0008.jpg
|       ├── 0009.jpg
|       ├── ...
```

In addition, the notebook will also perform Exploratory Data Analysis to check on:

- image basic components
- image width and height
- polyp positions
- polyp size and count
- image hue, brightness, and saturation

### *Image preprocessing Data generator and Modeling.ipynb*

This notebook covers four main sections, they are:

- Prepare image data generator for training the U-net model
- Evaluate the model performance using various metrics such as IoU (Intersaction over Union), Dice Coefficient, and a confusion matrix
- Recommend techniques to improve the model
- Discuss on model’s limitation