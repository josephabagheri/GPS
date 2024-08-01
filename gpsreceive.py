import time
import os
import numpy as np
from pyproj import CRS, Transformer
import folium


def save_gps_data(data, filename):
        with open(filename,"w") as file:
                file.write(data)

# Create file to  write to
counter = 1
savefilename = f"data/gps_data_{counter}.txt"

while os.path.exists(savefilename):
        # Increment the counter and create a new file name
        counter += 1
        savefilename = f"gps_data_{counter}.txt"

# Initialize the projection (WGS84 to UTM Zone 17)
wgs84 = CRS.from_epsg(4326)
utm = CRS.from_epsg(32617)  # EPSG code for UTM Zone 17N
transformer = Transformer.from_crs(wgs84, utm)

# Function to convert lat/lon to XY
def latlon_to_xy(lat, lon):
    x, y = transformer.transform(lat, lon)
    return x, y

# Function to parse the GPGGA string
def parse_gpgga(gpgga_str):
    try:
        parts = gpgga_str.split(',')
        if len(parts) < 6 or not parts[2] or not parts[4]:
            raise ValueError("Incomplete GPGGA string")
        lat = float(parts[2][:2]) + float(parts[2][2:]) / 60.0
        if parts[3] == 'S':
            lat = -lat
        lon = float(parts[4][:3]) + float(parts[4][3:]) / 60.0
        if parts[5] == 'W':
            lon = -lon
        return lat, lon
    except (IndexError, ValueError) as e:
        print(f"Error parsing GPGGA string: {e}")
        return '', ''


# Main loop to read the file and update the plot
filename = 'receive.txt'
last_line = None
latitude = 42.877821
longitude = -80.729561
# Create a map centered around your location
my_map = folium.Map(location=[latitude, longitude], zoom_start=15)
# Add a marker for your location
folium.Marker([latitude, longitude], tooltip='Your Location').add_to(my_map)
# Save the map as an HTML file
my_map.save("my_location_map.html")
while True:
    try:
        with open(filename, 'r') as file:
            first_line = file.readline().strip()
            if first_line != last_line:
                last_line = first_line
                lat, lon = parse_gpgga(first_line)
                if lat != '' and lon != '':
                    # Add a marker for your location
                    folium.Marker([lat, lon], tooltip='Your Location').add_to(my_map)
                    # Save the map as an HTML file
                    my_map.save("my_location_map.html")

                save_gps_data(first_line, savefilename)
    except (OSError, FileNotFoundError):
        print(f"File {filename} is not available. Retrying in 1 second...")
    time.sleep(1)  # Check for updates every second
