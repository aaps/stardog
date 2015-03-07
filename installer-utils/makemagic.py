
import sys, os
import Image

indexes = ["r","g","b"]

if len(sys.argv) > 2:

    img = Image.open(sys.argv[1])
    filename = os.path.split(sys.argv[1])
    pixeldata = img.load()
    
    toremove = indexes.index(sys.argv[2])
    tokeep = []
    
    for x in indexes:
        tokeep.append(indexes.index(x))
    tokeep.pop(toremove)

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            pix = list(pixeldata[x, y])
            pix[toremove] = 0
            average = ((pix[tokeep[0]] + pix[tokeep[1]]) / 2)
            pix[tokeep[0]] =  pix[tokeep[1]] = average
            pixeldata[x,y] = tuple(pix)
                

    img.save(filename[0] + '/' + filename[1])