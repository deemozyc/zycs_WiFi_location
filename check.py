# coding:utf-8
import csv
import matplotlib
import matplotlib.pyplot as plt

from base import *

def check6(coord):
	if(len(coord)%6!=0):
		print "NO!!!!!!!"
	for i in range(len(coord)/6):
		if(coord[6*i] != coord[6*i+1] or coord[6*i+1] != coord[6*i+2] or coord[6*i+2] != coord[6*i+3] or 
		coord[6*i+3] != coord[6*i+4] or coord[6*i+4] != coord[6*i+5]):
			print "xxxxxxxxxxxxxxxx"
		

for i in range(6):
	if(i == 0):
		continue
	if(i<10):
		filename = 'db/01/tst0' + str(i) + 'crd.csv'
	else:
		filename = 'db/01/tst' + str(i) + 'crd.csv'
	trn_coord = get_csv(filename)
	check6(trn_coord)
	print "ok"

