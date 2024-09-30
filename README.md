
# **WMS Image Fetching and Semantic Segmentation**

This project includes two main functionalities:
1. **Fetching satellite images from a WMS service** at half-hour intervals based on user-specified date ranges.
2. **Performing semantic segmentation** on the fetched images using a pre-trained DeepLabV3+ model with GPU acceleration.

## **1. Fetching WMS Images**

This script retrieves images from an OGC-compliant **WMS (Web Map Service)** at half-hour intervals starting from **00:15** for each day in the specified date range.

### **Usage Instructions**

1. **Install Required Packages**:
   Make sure you have the following Python packages installed:
   ```bash
   pip install requests Pillow
   ```

2. **Running the Script**:
   - **Input Parameters**: You will be prompted to enter a **start date** and **end date** in `YYYYMMDD` format (e.g., `20240915` for 15th September 2024).
   - The script will then download images at half-hour intervals between these dates from the WMS service.

3. **Image Storage**:
   - Images are saved in a folder called `wms_images` in the current working directory.
   - Each image is saved with a filename format: `wms_image_YYYYMMDD_HHMM.png`, where `HHMM` corresponds to the half-hour timestamp.

4. **Script Example**:
   ```bash
   python wms_image_fetcher.py
   ```

5. **Output**:
   - The script will display messages indicating successful downloads or errors.
   - Example message: `Image saved as 'wms_images/wms_image_20240915_0015.png'`

---

## **2. Semantic Segmentation**

This script uses a **pre-trained DeepLabV3+ model** to perform **semantic segmentation** on the fetched images. The model is run on-device, utilizing **GPU acceleration** if available.

### **Usage Instructions**

1. **Install Required Packages**:
   Make sure you have the following Python packages installed, along with TensorFlow's GPU version if you have a compatible GPU:
   ```bash
   pip install tensorflow-gpu opencv-python matplotlib
   ```

2. **Running the Segmentation Script**:
   - The script will load the images from the `wms_images` folder and apply semantic segmentation using the DeepLabV3+ model.
   - It checks for GPU availability and uses it for processing, ensuring faster segmentation with **parallel processing**.

3. **Segmentation Results**:
   - The segmented images are displayed using **Matplotlib** and can be saved to disk if needed.
   - Each image is processed and segmented, showing a comparison between the **original image** and the **segmented output**.

4. **Segmentation Script Example**:
   ```bash
   python segmentation.py
   ```

5. **Output**:
   The script will display the original image alongside the segmented version. You can modify the script to save the segmented images if required.

---

## **Project Files**

- **wms_image_fetcher.py**: This script fetches images from the WMS service at half-hour intervals between user-specified dates.
- **segmentation.py**: This script performs semantic segmentation on the fetched images using a pre-trained DeepLabV3+ model, with optional GPU acceleration.

---

## **Requirements**

- Python 3.x
- **Pillow**: For image handling and manipulation.
- **TensorFlow-GPU**: For performing semantic segmentation with GPU support (optional but recommended for faster processing).
- **OpenCV**: For image preprocessing and handling.
- **Matplotlib**: For visualizing the segmentation results.

---

## **Example Workflow**

1. **Fetch Images from WMS**:
   ```bash
   python wms_image_fetcher.py
   ```
   - Input the desired **start date** and **end date**.
   - Images will be saved in the `wms_images` directory.

2. **Perform Semantic Segmentation**:
   ```bash
   python segmentation.py
   ```
   - The script will process all images in the `wms_images` directory and display the segmentation results.

---

## **Future Enhancements**

- Add **multithreading** to download images in parallel for faster WMS data fetching.
- Implement **automated saving** of segmented images to the disk in the segmentation script.
- Add **customizable WMS parameters** (layers, styles, etc.) to allow more flexibility when fetching data.

---

## **Troubleshooting**

- Ensure that the WMS server URL is correct and accessible from your network.
- If the TensorFlow GPU version is not installed, the script will fall back to the CPU, which may result in slower processing.
- If you encounter issues with **image downloads**, check the WMS service status or network connectivity.

---
