import os,sys,time
import subprocess
import datetime

# 10 = RAW + Medium Fine JPEG
setupcommands=['gphoto2 --set-config capturetarget=1',
               'gphoto2 --set-config /main/imgsettings/imageformat=10']
getcommand='gphoto2 --get-all-files'
clearcommand='gphoto2 --delete-all-files --recurse'

delay=int(sys.argv[1])
if len(sys.argv)>2:
    npictures=int(sys.argv[2])
else:
    npictures=-1

for command in setupcommands:
    os.system(command)
    
picturecommand= 'gphoto2 --auto-detect --capture-image -F {} -I {}'.format(npictures, delay)

os.system(clearcommand)

os.system(picturecommand)

path= '/home/pi'
p=subprocess.Popen(getcommand.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
exitcode = p.returncode

os.system(clearcommand)
for line in out.split('\n'):
    if len(line.strip())==0:
        continue
    filename=line.split()[-1]
    fullpath= os.path.join(path,filename)   # concatenate path and filename
    timestamp= os.path.getmtime(fullpath) + 18000   # gets mtime of file and adjusts for timezone difference
    modifiedtimestamp = time.strftime('%Y%m%d%H%M%S', time.localtime(timestamp)) # hopefully puts mtime in proper format
    ext=filename.split('.')[-1]  # gets file extension
    newfilename='%s.%s' % (modifiedtimestamp, ext) 
    os.rename(filename, newfilename)
    print('Moved %s -> %s' % (filename, newfilename))



