import sys
import re
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from os.path import basename
from cvxpy import *

# Function that returns the super-resolved image
def super(i_list,g_size):
   image_list= []
   for i in range(0,group_size):
      image_list.append(np.array(Image.open(i_list.pop(0))))
   patch=20
   step=patch-2
   rows=image_list[0].shape[0]
   cols=image_list[0].shape[1]
   result = np.zeros(shape=(rows,cols))
   for l in xrange(0,rows,step):
      if l+patch > rows:
        l=rows-patch
      print "Percentage completed", (100*l)//rows
      for c in xrange(0,cols,step):
         if c+patch > cols:
            c=cols-patch
         U = Variable(patch, patch)
         obj = Minimize(sum(norm(image_list[i][l:l+patch,c:c+patch]-U) for i in range(g_size) )+tv(U))
         prob = Problem(obj, [])
         # Use SCS to solve the problem.
         prob.solve(verbose=False, solver=SCS)
         result[l+1:l+patch-1,c+1:c+patch-1]=U.value[1:patch-1,1:patch-1]
   return Image.fromarray(result)

#number of images to be grouped
group_size = 5


#Setting initial parameters
if len(sys.argv) < 2:
   print 'Instructions: lidarboost -g <group_size> image1 image2 image3...\nDefault group_size is ', group_size;
   sys.exit(0);
if sys.argv[1] == '-g':
   group_size= int(sys.argv[2])
   del sys.argv[1:3]
del sys.argv[0]
x=(len(sys.argv)//group_size)*group_size
del sys.argv[x:]

#sys.argv have the images filenames

#base holds the savename
pos = re.search("\d",sys.argv[0]).start()
base= basename(sys.argv[0][0:pos])


for i in range(0,len(sys.argv)//group_size):
   new_image=super(sys.argv,group_size)
   if new_image.mode != 'RGB':
      new_image = new_image.convert('RGB')
   new_image.save("out/"+base+str(i)+".png")


