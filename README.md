# Polyp Segmentation Tool

## Overview

This Polyp Segmentation Tool is designed to assist healthcare professionals by providing an automated way to segment polyps from colonoscopy images. Utilizing a deep learning model based on the U-Net architecture, this tool aims to enhance the preliminary diagnosis process and aid in treatment planning by offering visual segmentation masks of detected polyps.

![alt text](https://production-media.paperswithcode.com/datasets/Screenshot_from_2021-05-05_23-44-10.png)

## Features

- **Automated Polyp Segmentation**: Users can upload colonoscopy images to receive segmentation masks that highlight polyp locations, facilitating early detection and diagnosis.
- **Streamlit Web Application**: The tool features a user-friendly web interface hosted on Streamlit Community Cloud, enabling easy uploading of colonoscopy images and visualization of segmentation results.
- **Flexible Upload Options**: Supports both single and multiple image uploads, catering to diverse diagnostic needs.
- **Downloadable Results**: Users can download segmentation masks as ZIP files for further analysis, documentation, or record-keeping.

## Technical Highlights

- **Deep Learning Model Optimization**: Employed a U-Net architecture, fine-tuned for high accuracy in medical image segmentation, demonstrating the effective application of established AI models to address specific challenges in medical diagnostics.
- **Data Preprocessing and Augmentation**: Highlighted the implementation of a robust pipeline for image resizing, normalization, and augmentation to improve model generalizability across different colonoscopy images.
- **Streamlined Interface and Dynamic Model Access**: Developed a Streamlit web application that prioritizes ease of use. The application supports batch processing and provides downloadable results for offline analysis. The deep learning model used for segmentation is securely stored on AWS S3 and is dynamically loaded by the application as needed.
- **Exploratory Data Analysis (EDA)**: Conducted detailed EDA to gain insights into polyp characteristics, which informed the preprocessing and augmentation strategies to enhance detection accuracy.

## Usage

1. **Access the Tool**: Navigate to the Streamlit app URL.
    [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://polyp-segmentation-tool.streamlit.app)

2. **Upload Images**: Use the file uploader to select colonoscopy images (JPG/JPEG) for segmentation.

3. **Process Images**: Click 'Process Images' to start the segmentation process.

4. **View and Download Results**: Segmentation masks are displayed alongside the original images. A ZIP file containing all masks can be downloaded.

[![App Demo](.streamlit/app_demo.gif)](https://polyp-segmentation-tool.streamlit.app/)