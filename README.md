# python_hdhomerun
This script was something I found on the internet last year but I can't find where that was. Regardless I modified this to get it working. This is only for Python 2 and doesn't work with Python 3. I tried to update it but that wasn't easy to I just kept it as is for now. 

I have an HD Home Run and it's hard to get much over the air info on channels but this little script helps. 

The script creates and xml file and then I run a script to send that file to the external xmltv socket with socat. 

cat hdhomerun.xml | socat - UNIX-CONNECT:/home/hts/.hts/tvheadend/epggrab/xmltv.sock
