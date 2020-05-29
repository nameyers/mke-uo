import os,sys,time
import subprocess
import datetime

# 10 = RAW + Medium Fine JPEG
setupcommands=['gphoto2 --set-config capturetarget=1',
               'gphoto2 --set-config /main/imgsettings/imageformat=10']
picturecommand='gphoto2 --auto-detect --capture-image'
getcommand='gphoto2 --get-all-files'
clearcommand='gphoto2 --delete-all-files --recurse'

delay=int(sys.argv[1])
if len(sys.argv)>2:
    npictures=int(sys.argv[2])
else:
    npictures=-1

for command in setupcommands:
    os.system(command)

i=0
os.system(clearcommand)
while (npictures<0) or (i<npictures):
    print('Exposing %03d / %03d' % (i,npictures))
    os.system(picturecommand)
    now=datetime.datetime.now()
    p=subprocess.Popen(getcommand.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    exitcode = p.returncode
    os.system(clearcommand)
    for line in out.split('\n'):
        if len(line.strip())==0:
            continue
        filename=line.split()[-1]
        ext=filename.split('.')[-1]
        newfilename='%s.%s' % (now.strftime('%Y%m%dT%H%M%S'),ext)
        os.rename(filename,newfilename)
        print('Moved %s -> %s' % (filename, newfilename))
    print('Waiting %d s...' % delay)
    time.sleep(delay)
    i+=1
    
    

