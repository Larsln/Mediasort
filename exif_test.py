import exiftool

def extract_metadata(video_path):
    with exiftool.ExifTool() as et:
        # Execute ExifTool and get metadata as a dictionary
        metadata = et.execute_json(video_path)
        return metadata

# Example usage
video_file = "./output/IMG_2834.HEIC"
metadata = extract_metadata(video_file)

#string = metadata[0]['QuickTime:GPSCoordinates']
#float_array = [float(value) for value in string.split()]
#print(float_array)
# Display metadata
if metadata:
    for tag, value in metadata[0].items():  # metadata[0] because execute_json returns a list
        print(f"{tag}: {value}")

