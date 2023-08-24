# arduverse
Project files and source code for making a real-time streaming from arduino to omniverse


Clone/download the repo. You should be able to just open the usda file in *PuppetScene* folder. 
To use:
- Upload the *UDP_FilteredAngle.ino* file to an arduino (RP2040 is what I used). 
- Make sure to change the wifi network credentials to your own
- Try to run the *udp.py* file to make sure the arduino is connecting and sending data
- If the udp to python connection is working, you should be able to get the scene running. 
- To use the base file, in omniverse create a python behavior script on any xform, and attach the script (e.g. *puppet_handle_1.py*)

Open an issue if you have problems. Also if you want to contribute go for it. 