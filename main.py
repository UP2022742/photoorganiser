import os
from PIL import Image
import shutil
from datetime import datetime as DateTime
import struct
import datetime

path = os.getcwd()

def get_img_timestamp(filename):
    try:

        # Open the image will pillow.
        img = Image.open(filename)

        # Using the Pillow module to find inital creation date on photoshot.
        # This will not work sometimes as metadata will not always be
        # captured. It will not work on screenshots either because they were
        # not taken with a camera.
        try: 
            pil_date_time = img._getexif().get(36867)
        except:
            pil_date_time = None

        # If it receives nothing from PILLOW will compare Windows values
        # creation vs modified as windows can often fuck this up and get
        # them the wrong way, this will find the lowest date and then use
        # that as the folder destination.
        
        if pil_date_time == None:   
            try:
                # Try initial time digitised or uploaded.
                modified_time = os.path.getmtime(filename)
                modified_time = str(modified_time).partition(' ')
                modified_time = modified_time[0].replace(":",".")

                creation_time = os.path.getctime(filename)
                creation_time = str(creation_time).partition(' ')
                creation_time = creation_time[0].replace(":",".")

                if modified_time < creation_time:
                    pil_date_time = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
                else:
                    pil_date_time = datetime.datetime.fromtimestamp(os.path.getctime(filename))

            # There is no overwrting from the None value so just leave this as a catch
            # and a print statement. 
            except:
                print("[Info] Unable to find metadata, this file will go in None.")

        # Need to close the image before moving it otherwise this process will
        # stop the moving of the file.
        img.close()
        return pil_date_time
    except Exception as e:
        print("[Debugging] ", e)
        print("[Info] There may be a corrupt file, all corrupt files are moved to '/Corrupt Files' relative to your current directory.")
        return "Corrupt Files"

def get_mov_timestamps(filename):
    ATOM_HEADER_SIZE = 8
    # difference between Unix epoch and QuickTime epoch, in seconds
    EPOCH_ADJUSTER = 2082844800

    creation_time = None
    try: 
        # search for moov item
        with open(filename, "rb") as f:
            while True:
                atom_header = f.read(ATOM_HEADER_SIZE)
                if atom_header[4:8] == b'moov':
                    break  # found
                else:
                    atom_size = struct.unpack('>I', atom_header[0:4])[0]
                    f.seek(atom_size - 8, 1)

            # found 'moov', look for 'mvhd' and timestamps
            atom_header = f.read(ATOM_HEADER_SIZE)
            if atom_header[4:8] == b'cmov':
                raise RuntimeError('moov atom is compressed')
            elif atom_header[4:8] != b'mvhd':
                raise RuntimeError('expected to find "mvhd" header.')
            else:
                f.seek(4, 1)
                creation_time = struct.unpack('>I', f.read(4))[0] - EPOCH_ADJUSTER
                creation_time = DateTime.fromtimestamp(creation_time)
                if creation_time.year < 1990:  # invalid or censored data
                    creation_time = "None"
        f.close()
        return creation_time
    except:
        print("There may be a corrupt MP4 or MOV file, these have been moved to Corrupt Files folder for reviewing.")
        return "Corrupt Files"

def file_formatting(filename, pil_date_time):
    # This is used to disquinguish if there was a file in which the program was
    # unable to rad the metadata for, if so it will simply skip the formatting
    # used for writing the dates for the corresponding folder as it's written
    # to the folder named 'none'.
    try:
        pil_date_time = pil_date_time.replace(":","-")
    except:
        print("[Info] There was a file that I was unable to read the metadata for, this has been moved to the None folder.")

    pil_date_time = pil_date_time.partition(' ')

    # If there is no existing directory for the day or the error handling folders
    # this will create one.
    if not os.path.exists(pil_date_time[0]):
        try:
            os.mkdir(pil_date_time[0])
        except OSError:
            print ("Creation of the directory /%s failed" % pil_date_time[0])
        else:
            print ("Successfully created the directory /%s" % pil_date_time[0])

    # Move file to its corresponding folder including both the error handling
    # and the date based ones.
    shutil.move(filename,pil_date_time[0])

def main(path):
    # For all the files in the current directory iterate through and see if they
    # follow the following file extensions if so run the script if not ignore 
    # them. 
    for filename in os.listdir(path):
        lower_file = filename.lower()
        if lower_file.endswith(".jpg") or lower_file.endswith(".png") or lower_file.endswith(".jpeg"):
            pil_date_time = get_img_timestamp(filename)
            file_formatting(filename, str(pil_date_time))

        elif lower_file.endswith('.mp4') or lower_file.endswith(".mov"):
            pil_date_time = get_mov_timestamps(filename)
            file_formatting(filename, str(pil_date_time))

    print("[Success] Script finished succesfully.")

if __name__ == "__main__":
    main(path)