# SPACE INSTAGRAM
Scrip get photos from space X last launches and Hubble collection and save them on 
selected instagram account.

## How to install:
 - Python3 should be already installed on PC.
 - Python dependencies file is `requirements.txt`.
 - Execute in command line `pip3 install -r requirements.txt` to install dependencies
 - You should put your instagram login and password in `.env` file at the same directory.  
       `login='your_login'`    
        `password='your_password'`
 
 
 ## How it works
 - Execute `python fetch_spacex.py` to get last spacex launch photos.
 If there no photos from the last launch script will search until it get some nice photos 
 from another launch.
 
- Execute `python fetch_hubble.py` to get photos from the Hubble collection.
 
- Both 'fetch' scripts  could be execute with -f parameter which allow you to specify
directory for images saving. Example:  
    `python fetch_hubble.py -f my_folder`  
    will create `my_folder` folder and put all parsed images in it.
if parameter -f not specified script will create by default folder `image`.

- Script `posting.py` will post post all photos from image directory to specified instagram account.
Due to Instagram policy some photos might be banned or library which script depends on might not
work. To run posting execute `python posting.py`.



