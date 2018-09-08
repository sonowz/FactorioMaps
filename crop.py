from PIL import Image
import multiprocessing as mp
import os, math, sys, time
from functools import partial



    
ext = ".jpg"

def work(line, imgsize, folder):
    arg = line.rstrip('\n').split(" ")
    path = "%s%s/%s%s" % (folder, arg[0], arg[1], ext)
    top = int(arg[2])
    left = int(arg[3])
    try:
        Image.open(path).crop((top, left, top + imgsize, left + imgsize)).save(path, format='JPEG', subsampling=0, quality=100)
    except IOError:
        return line
    return False

        


if __name__ == '__main__':

    toppath = (sys.argv[2] if len(sys.argv) > 2 else "../../script-output/FactorioMaps/Test") + "/"
    folder = os.path.join(toppath, "Images/", (sys.argv[1] if len(sys.argv) > 1 else "Night") + "/20/")
    datapath = os.path.join(toppath, "crop-" + (sys.argv[1] if len(sys.argv) > 1 else "Night") + ".txt")
    maxthreads = mp.cpu_count()

    print(folder)
    
    files = []
    with open(datapath, "r") as data:
        imgsize = int(data.readline().rstrip('\n'))
        for line in data:
            files.append(line)
    
    pool = mp.Pool(processes=maxthreads)
    while len(files) > 0:
        print("left: %s" % len(files))
        files = filter(lambda x: x, pool.map(partial(work, imgsize=imgsize, folder=folder), files, 128))
        time.sleep(2.5)


