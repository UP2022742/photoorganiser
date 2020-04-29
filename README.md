# Photo Organiser
Organises photos into folders based on their date of creation. The script will also check the validity of the photo making sure that it isn't corrupt, if it is it will placed inside of a folder called "Corrupt Files". If the metadata isn't readable these phtotos will be placed inside of a folder called "None". 

# Before & After
<img src="before%20&%20after/before.PNG" width="50%"><img src="before%20&%20after/after.jpg" width="50%">

# Warning
Have not tested on Linux, this will likely have issues with Ubuntu but it should be a simply fix once I get time. Only Windows tested for now.

# Usage
- Automated
Simply clone the repo or download the EXE file and place it into a folder with the photos you'd like to start and run it. The script will automatically close once complete.
- Manual
In order to install it manually, you most clone the repo and install pillow by running the command in console.
"pip install pillow". Once thatm is complete you should be able to execute the python script with "python ./main.py" this was made with python 3.x.
