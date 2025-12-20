import os
import time
import logging
logging.basicConfig(level=logging.INFO, format = " %(asctime)s - %(levelname)s - %(message)s")
#logging.disable(logging.CRITICAL) # COMMENT OUT THIS LINE TO DISABLE LOGGING MESSAGES

# All file locations
tts_dir = "./tts"
tts_file = "tts1.wav"
tts_path = os.path.join(tts_dir, tts_file)
base_tts_file = "tts.wav"

image_dir = "./images"
image_file = "example6.jpg"
image_path = os.path.join(image_dir, image_file)
base_image_file = "image.jpg"

ocr_dir = "./ocr"
ocr_file = "ocr1.txt"
ocr_path = os.path.join(ocr_dir, ocr_file)
base_ocr_file = "ocr.txt"

current_dir = os.getcwd()

"""
    Make directories if they do not exist
"""
def init_folders():
    print("I AM RAISING HELL FOR SOME REASON")
    logging.info("Creating necessary directories")

    for path in (tts_dir, image_dir, ocr_dir):
        os.makedirs(path, exist_ok=True)
        logging.info(f"Ensured directory exists: {path}")

"""
    This function shifts files and renames them to open space
    for a new file.
    Takes a parameter for the directory we wish to perform the shift in,
    the base name of the file that we wish to perform actions on, and the
    maximum number of those files we want to keep.
    e.g. 
        directory = ./testing
        base_name = test.txt
        max_num_of_files = 4

        ./testing/test5.txt -> deleted
        ./testing/test4.txt -> deleted
        ./testing/test3.txt -> test4.txt
        ./testing/hello.wav -> unaffected
        ./testing/test2.txt -> test3.txt
        ./testing/test.py   -> unaffected
        ./testing/test.txt  -> unaffected
        ./testing/test1.txt -> test2.txt

        This allows us to create a new test1.txt elsewhere in the program 
        and not overwrite any old files.
    
    By default checks in the project folder directory and only allows for
    one file of the base_name type.
"""
def shift_files(base_name: str, directory = ".", max_num_of_files = 1):

    # Make sure that the passed directory is a string and exists.
    assert isinstance(directory, str), "directory must be passed as a string"
    assert os.path.exists(directory), "Error finding directory"
    
    # Make sure that the passed base_name is a string and that a "." exists
    # somewhere in the file name.
    assert isinstance(directory, str), "directory must be passed as a string"
    assert "." in base_name, "base_name must contain a . somewhere in the string"

    # Make sure that max_num_of_files is an integer

    assert isinstance(max_num_of_files, int), "max_num_of_files must be an integer"
    # Split the string at the last "." to split the name and file extension.
    # Returns a tuple containing the prefix, delimiter, and postfix.
    # of the string.
    parts = base_name.partition(".") 
    logging.info(f"Rarts of the base name are {parts}")

    # Make sure that at least one file of the type base_name exists in the directory
    # passed. Return if not found.
    test_file = f"{parts[0]}1{parts[1]}{parts[2]}"
    test_file_path = os.path.join(directory, test_file)
    logging.info(f"Looking for {test_file_path}")
    if not (os.path.isfile(test_file_path)):
        logging.warning(f"Could not find {test_file_path}")
        return
    else:
        logging.info(f"Found {test_file_path}")

    # Define a path for the largest possible numbered file
    count_up = 0
    file = f"{parts[0]}{max_num_of_files + count_up}{parts[1]}{parts[2]}"
    file_path = os.path.join(directory, file)
    logging.info(f"Defined path for {file_path}")
    
    # Delete extra files
    while(os.path.isfile(file_path)):
        os.remove(file_path)
        logging.info(f"Removed {file_path}")
        count_up += 1
        file = f"{parts[0]}{max_num_of_files + count_up}{parts[1]}{parts[2]}"
        file_path = os.path.join(directory, file)

    file_new = f"{parts[0]}{max_num_of_files}{parts[1]}{parts[2]}"
    file_new_path = os.path.join(directory, file_new)
    # Shift remaining files
    for i in range(max_num_of_files, 1, -1):
        file_current = f"{parts[0]}{i - 1}{parts[1]}{parts[2]}"
        file_current_path = os.path.join(directory, file_current)
        if(os.path.isfile(file_current_path)):
            os.rename(file_current_path, file_new_path)
            logging.info(f"Shifted up {file_current_path} to {file_new_path}")
        else:
            logging.info(f"{file_current_path} does not exist")
        file_new = file_current
        file_new_path = os.path.join(directory, file_new)