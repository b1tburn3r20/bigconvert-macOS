import os
import zipfile
import ffmpeg

# Constants
SOURCE_DIR = "/Users/alejandrobermudez/Desktop/wmafiles/"
DESTINATION_DIR = "/Users/alejandrobermudez/Desktop/convertedmp3/"

# State variables
file_index = 0
converted_files = []

# Functions


def convert_wma_to_mp3(source_file, destination_file):
    # Converts a WMA file to MP3 format
    try:
        stream = ffmpeg.input(source_file)
        stream = ffmpeg.output(stream, destination_file, format="mp3")
        ffmpeg.run(stream)
        print("File converted:", source_file)
        return True
    except ffmpeg.Error as e:
        print("An error occurred while converting the file:", source_file)
        print(e.stderr.decode('utf-8'))
        return False


# Main code
if __name__ == "__main__":
    # Create a temporary directory for the converted files
    temp_dir = os.path.join(DESTINATION_DIR, "temp")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Iterate over all files in the source directory
    for filename in os.listdir(SOURCE_DIR):
        # Check if the file is a WMA file
        if filename.endswith(".wma"):
            # Construct the source and destination file paths
            source_file = os.path.join(SOURCE_DIR, filename)
            destination_file = os.path.join(temp_dir, filename[:-4] + ".mp3")

            # Convert the file from WMA to MP3 format
            if convert_wma_to_mp3(source_file, destination_file):
                file_index += 1
                converted_files.append(destination_file)

    # Zip the converted files into a single archive
    base_dir_name = "wma-to-mp3Files"
    zip_file_path = os.path.join(os.path.dirname(
        DESTINATION_DIR), base_dir_name + ".zip")
    with zipfile.ZipFile(zip_file_path, "w") as zip_file:
        for file_path in converted_files:
            # Write only the file name without any directory
            zip_file.write(file_path, os.path.basename(file_path))

    # Remove the temporary directory
    for file_path in converted_files:
        os.remove(file_path)
    os.rmdir(temp_dir)

    # Send the archive to the user for download
    # <code to send the archive to the user>
