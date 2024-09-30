import requests
from PIL import Image
from io import BytesIO
from datetime import datetime, timedelta
import os

# Function to generate half-hour intervals starting at 00:15 for a given date
def generate_half_hour_timestamps(date, is_end_date=False):
    start_time = datetime.combine(date, datetime.min.time()) + timedelta(minutes=15)  # Start at 00:15 of the given date
    end_time = datetime.combine(date, datetime.max.time())  # Default end time is 23:59 of the given date
    if is_end_date:  # For the end date, stop at the current time if it's today
        end_time = min(datetime.combine(date, datetime.max.time()), datetime.now())
    timestamps = []
    while start_time <= end_time:
        timestamps.append(start_time.strftime('%H%M'))  # Generate time in HHMM format
        start_time += timedelta(minutes=30)  # Increment by 30 minutes
    return timestamps

# Get the start date input from the user (format: YYYYMMDD)
start_input = input("Enter the start date in YYYYMMDD format (e.g., 20240915 for 15th September 2024): ")
try:
    start_date = datetime.strptime(start_input, '%Y%m%d').date()  # Parse the start date
except ValueError:
    print("Invalid start date format. Please enter in YYYYMMDD format.")
    exit()

# Get the end date input from the user (format: YYYYMMDD)
end_input = input("Enter the end date in YYYYMMDD format (e.g., 20240916 for 16th September 2024): ")
try:
    end_date = datetime.strptime(end_input, '%Y%m%d').date()  # Parse the end date
except ValueError:
    print("Invalid end date format. Please enter in YYYYMMDD format.")
    exit()

# Validate that the end date is not before the start date
if end_date < start_date:
    print("End date cannot be earlier than the start date.")
    exit()

# Directory to save the images
output_dir = "wms_images"
os.makedirs(output_dir, exist_ok=True)  # Create the folder if it doesn't exist

# Loop through each day from start_date to end_date (inclusive)
current_date = start_date
while current_date <= end_date:
    # Generate timestamps for the current day (for the end date, handle the current time)
    is_end_date = (current_date == end_date)  # Mark if it's the final day
    timestamps = generate_half_hour_timestamps(current_date, is_end_date)

    # Base URL for the WMS service (use the current date in the URL)
    base_url = f"https://mosdac.gov.in/live_data/wms/live3RL1BSTD4km/products/Insat3r/3R_IMG/{current_date.strftime('%Y')}/{current_date.strftime('%d%b').upper()}/3RIMG_{current_date.strftime('%d%b').upper()}{current_date.strftime('%Y')}_"

    # Common WMS parameters
    wms_params = "_L1B_STD_V01R00.h5?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image/png&TRANSPARENT=true&LAYERS=IMG_TIR1&COLORSCALERANGE=315,929&BELOWMINCOLOR=extend&ABOVEMAXCOLOR=extend&transparent=true&format=image/png&STYLES=boxfill/greyscale&singleTile=true&ratio=1&CRS=EPSG:3857&WIDTH=871&HEIGHT=782&BBOX=4579514.378564888,-882744.3739599851,13101325.788022619,6768296.409273017"

    # Loop through all timestamps for the current date and fetch the images
    for timestamp in timestamps:
        # Construct the full URL for each time
        wms_url = f"{base_url}{timestamp}{wms_params}"

        # Fetch the image from the WMS server
        response = requests.get(wms_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Load image into memory
            img = Image.open(BytesIO(response.content))

            # Save the image to a file in the 'wms_images' folder with the corresponding timestamp
            img_filename = os.path.join(output_dir, f"wms_image_{current_date.strftime('%Y%m%d')}_{timestamp}.png")
            img.save(img_filename)

            print(f"Image saved as '{img_filename}'")
        else:
            print(f"Failed to fetch the image for timestamp {timestamp}. Status code: {response.status_code}")

    # Increment the date by 1 day
    current_date += timedelta(days=1)
