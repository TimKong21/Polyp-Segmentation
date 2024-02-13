import streamlit as st
import os
import boto3
import shutil
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image
from zipfile import ZipFile

# Function to download the model from S3
def download_model_from_s3(bucket_name, object_key, model_path):
    # Ensure the directory for the model exists
    model_dir = os.path.dirname(model_path)
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        print(f"Created directory {model_dir} for model.")

    if not os.path.exists(model_path):
        print("Model not found locally. Downloading from S3...")
        s3 = boto3.client('s3')
        s3.download_file(Bucket=bucket_name, Key=object_key, Filename=model_path)
        print("Model downloaded.")
    else:
        print("Model found locally. Loading...")

# Function to load the model, ensuring it's downloaded if not present
def load_model(model_path):
    # Define S3 bucket details and local model path
    bucket_name = 'segmentation-model-bucket'
    object_key = 'model/unet.h5'

    # Download the model from S3
    download_model_from_s3(bucket_name, object_key, model_path)

    # Load and return the model
    model = tf.keras.models.load_model(model_path)
    return model

# Function to clear the temporary directory
def clear_temp_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory, exist_ok=True)

# Function to generate data batches
def generate_data_batches(data_dir, batch_size, target_size, seed=None):
    # Rescaling factor for all sets
    rescale_factor = 1.0 / 255.0

    # Set random seed if provided
    if seed is not None:
        np.random.seed(seed)

    # Data generator for test sets (without augmentation)
    test_data_generator = ImageDataGenerator(rescale=rescale_factor)

    test_images_generator = test_data_generator.flow_from_directory(
        data_dir + '/app_images',
        target_size=target_size,
        batch_size=batch_size,
        class_mode=None,
        shuffle=False,  # Unshuffle to maintain the original order for proper prediction
        seed=seed
    )

    return test_images_generator

# Function to handle uploaded files and predictions
def process_and_display_images(loaded_model, uploaded_files, temp_dir):
    try:
        # Clear and recreate the temporary directory
        clear_temp_directory(temp_dir)

        # Directory to save individual masks (temporarily)
        masks_dir = os.path.join(temp_dir, "masks")
        os.makedirs(masks_dir, exist_ok=True)

        # Save uploaded files to the temporary directory
        for uploaded_file in uploaded_files:
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

        # Generate data batches
        batch_size = 16
        test_images_gen = generate_data_batches('./temp_app_data/', batch_size, (256, 256), seed=123)

        # Calculate the number of steps needed to process all uploaded files
        total_files = len(uploaded_files)
        steps_needed = np.ceil(total_files / batch_size)

        # Initialize a global index to track the original file names across batches
        global_index = 0

        # Process and display each batch of images
        for _ in range(int(steps_needed)):
            batch = next(test_images_gen)
            predictions = loaded_model.predict(batch)
            binary_predictions = (predictions > 0.5).astype(np.uint8)

            for j, pred_image in enumerate(binary_predictions):
                if global_index >= len(uploaded_files):
                    break  # Break if global index exceeds the number of uploaded files

                # Convert binary prediction to image
                pred_pil_image = Image.fromarray(pred_image.squeeze() * 255)

                # Create two columns for original image and predicted mask
                col1, col2 = st.columns(2)

                # Display original image in the first column
                with col1:
                    original_image = Image.open(uploaded_files[global_index])
                    st.image(original_image, caption='Original Image', use_column_width=True)

                # Display predicted mask in the second column
                with col2:
                    st.image(pred_pil_image, caption='Predicted Mask', use_column_width=True)

                # Use the global index to get the correct uploaded file name
                original_file_name = os.path.basename(uploaded_files[global_index].name)
                original_name_without_ext = os.path.splitext(original_file_name)[0]
                mask_filename = f"mask_{original_name_without_ext}.jpg"
                mask_path = os.path.join(masks_dir, mask_filename)
                pred_pil_image.save(mask_path, "JPEG")

                # Increment the global index after processing each image
                global_index += 1

        # After processing all images, create a ZIP file of all masks
        zip_path = os.path.join(temp_dir, "masks.zip")
        with ZipFile(zip_path, 'w') as zipf:
            for mask_file in os.listdir(masks_dir):
                zipf.write(os.path.join(masks_dir, mask_file), arcname=mask_file)

        # Provide a download button for the ZIP file
        with open(zip_path, "rb") as f:
            st.download_button(
                label="Download All Masks as ZIP",
                data=f.read(),
                file_name="masks.zip",
                mime="application/zip"
            )

        # Clean up: Delete the temporary directory
        shutil.rmtree('./temp_app_data')
        
    except Exception as e:
        st.error(f"An error occurred while processing the images: {e}")

def main():
    # Load the model
    model_path = 'model/unet.h5'
    model = load_model(model_path)

    # App title
    st.title("Polyp Segmentation Tool")

    # Embedding an image from a URL after the title
    image_url = "https://production-media.paperswithcode.com/datasets/Screenshot_from_2021-05-05_23-44-10.png"
    st.image(image_url, use_column_width=True)

    # Step 1: Explanatory Notes or Guidance
    st.header("How to Use This Tool")
    st.write("""
        This tool allows healthcare professionals to upload colonoscopy images and receive automated polyp segmentation. 
        Here's how to interpret the results:
        
        - The segmentation mask visually highlights the areas identified as polyps.
        - Users can visually assess the size and shape of the polyps using the mask as a guide.
        - For quantitative measurements, users can manually measure the dimensions of the polyps based on the mask.
        - This visual aid assists in preliminary diagnosis and determining the need for further investigation.
        
        Supported file formats: jpg, jpeg.
    """)

    # Link for downloading sample images
    st.markdown("Download sample colonoscopy images to test the app [here](https://github.com/TimKong21/Polyp-Segmentation/tree/main/new_data/test/images/test).")

    # Step 2: Upload Interface
    st.header("Upload Colonoscopy Images")
    st.write("Upload single or multiple JPG/JPEG images for polyp segmentation.")
    st.markdown("""
    _**Note:** To deselect files, clear the selection by clicking the "x" next to the uploaded files in the file uploader widget, or simply refresh the browser for a new session._
    """, unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Choose images", accept_multiple_files=True, type=['jpg', 'jpeg'])
    

    # Temporary directory for uploaded files
    temp_dir = './temp_app_data/app_images/test'

    # Step 3: Process and display images after Process button is being pressed
    if uploaded_files:
        if st.button('Process Images'):
            with st.spinner('Processing images...'):
                process_and_display_images(model, uploaded_files, temp_dir)
                st.success('Processing complete!')
               
if __name__ == "__main__":
    main()