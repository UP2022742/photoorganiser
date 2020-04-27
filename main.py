import os
import PIL.Image
import shutil
from datetime import datetime as DateTime
import struct

path = os.getcwd()
print("This the current directory is %s." % path)

def get_img_timestamp(filename):
    # Use Pillow to read and collect metadata.
    img = PIL.Image.open(filename)
    pil_date_time = img._getexif().get(36867)
    img.close()
    return pil_date_time

def get_mov_timestamps(filename):
    ATOM_HEADER_SIZE = 8
    # difference between Unix epoch and QuickTime epoch, in seconds
    EPOCH_ADJUSTER = 2082844800

    creation_time = None

    # search for moov item
    with open(filename, "rb") as f:
        while True:
            atom_header = f.read(ATOM_HEADER_SIZE)
            #~ print('atom header:', atom_header)  # debug purposes
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
                creation_time = None
    f.close()
    return str(creation_time)

def file_formatting(filename, pil_date_time):
    # Remove colons and split the date time into an array.
    pil_date_time = pil_date_time.replace(":","-")
    pil_date_time = pil_date_time.partition(' ')

    # If there is no directory for the day create one.
    if not os.path.exists(pil_date_time[0]):
        try:
            os.mkdir(pil_date_time[0])
        except OSError:
            print ("Creation of the directory /%s failed" % pil_date_time[0])
        else:
            print ("Successfully created the directory /%s" % pil_date_time[0])

    # Move file to its corresponding folder for the day.
    shutil.move(filename,pil_date_time[0])

for filename in os.listdir(path):
    lower_file = filename.lower()
    if lower_file.endswith(".jpg") or lower_file.endswith(".png"):
        pil_date_time = get_img_timestamp(filename)
        file_formatting(filename, pil_date_time)

    elif lower_file.endswith('.mp4') or lower_file.endswith(".mov"):
        pil_date_time = get_mov_timestamps(filename)
        file_formatting(filename, pil_date_time)