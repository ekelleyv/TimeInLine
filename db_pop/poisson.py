from math import exp
from random import random

def poisson(lambd):
  L = exp(-lambd)
  print "L:",L
  k = 0
  p = 1

  k=k+1
  u = random()
  p = p * u
  while p > L:
    k = k + 1
    u = random()
    p = p * u
  print "ret: ",k - 1
  return k -1

if __name__ == '__main__':
  lambd = long(raw_input("Enter lambda:"))
  rvals = []
  for i in range(100):
    rvals.append(poisson(lambd))
  counts = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  for i in range(100):
    counts[rvals[i]] += 1

  print "rvals: ",rvals
  print "\n\n counts: ",counts


