import sys
import re
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from os.path import basename
from cvxpy import *

# Funcao que retorna imagem super-resolvida
def super(lista,tam):
   limagens= []
   for i in range(0,tgrupo):
      limagens.append(np.array(Image.open(lista.pop(0))))
   patch=20
   step=patch-2
   linhas=limagens[0].shape[0]
   colunas=limagens[0].shape[1]
   resultado = np.zeros(shape=(linhas,colunas))
   for l in xrange(0,linhas,step):
      if l+patch > linhas:
        l=linhas-patch
      print "porcentagem completa ", (100*l)//linhas
      for c in xrange(0,colunas,step):
         if c+patch > colunas:
            c=colunas-patch
         U = Variable(patch, patch)
         obj = Minimize(sum(norm(limagens[i][l:l+patch,c:c+patch]-U) for i in range(tam) )+tv(U))
         prob = Problem(obj, [])
         # Use SCS to solve the problem.
         prob.solve(verbose=False, solver=SCS)
         resultado[l+1:l+patch-1,c+1:c+patch-1]=U.value[1:patch-1,1:patch-1]
   return Image.fromarray(resultado)


tgrupo = 5


#Acertando parametros de entrada
if len(sys.argv) < 2:
   print 'Instructions: lidarboost -g <group_size> image1 image2 image3...\nDefault group_size is ', tgrupo;
   sys.exit(0);
if sys.argv[1] == '-g':
   tgrupo= int(sys.argv[2])
   del sys.argv[1:3]
del sys.argv[0]
x=(len(sys.argv)//tgrupo)*tgrupo
del sys.argv[x:]

#sys.argv agora carrega o nome de cada arquivo que sera super resolvido

#base vai carregaro nome o arquivo sem os numeros e extensao para facilitar gravamento posterior
pos = re.search("\d",sys.argv[0]).start()
base= basename(sys.argv[0][0:pos])

#print sys.argv
for i in range(0,len(sys.argv)//tgrupo):
#    super(sys.argv,tgrupo)
   novaimagem=super(sys.argv,tgrupo)
   if novaimagem.mode != 'RGB':
      novaimagem = novaimagem.convert('RGB')
   novaimagem.save("out/"+base+str(i)+".png")


