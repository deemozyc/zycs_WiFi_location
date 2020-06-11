# coding:utf-8
from sklearn import svm
from sklearn.svm import SVC
import csv
import matplotlib
import matplotlib.pyplot as plt

from base import *

def print_base(): #输出采集点地图
	tst_coord = get_csv('db/02/tst01crd.csv')
	tst_coord =  coord_zip(tst_coord)
	fig,ax = plt.subplots()
	plt.axis([2, 16, 14, 32])

	plt.scatter([ i[0] for i in  tst_coord], [i[1] for i in tst_coord])
	"""
	plt.plot([6,6],[14,32],color="red")
	plt.plot([11,11],[14,32],color="red")
	plt.plot([2,16],[21,21],color="red")
	plt.plot([2,16],[25,25],color="red")
	"""
	#画书架
	shelve_coord = get_shelve_coord()
	for i in range(0,len(shelve_coord),4): #4个坐标一个书架
		x_min = min(shelve_coord[i][0], shelve_coord[i+1][0], shelve_coord[i+2][0], shelve_coord[i+3][0])
		x_max = max(shelve_coord[i][0], shelve_coord[i+1][0], shelve_coord[i+2][0], shelve_coord[i+3][0])
		y_min = min(shelve_coord[i][1], shelve_coord[i+1][1], shelve_coord[i+2][1], shelve_coord[i+3][1])
		y_max = max(shelve_coord[i][1], shelve_coord[i+1][1], shelve_coord[i+2][1], shelve_coord[i+3][1])
		
		rect = mpathes.Rectangle([x_min, y_min],x_max-x_min, y_max-y_min,color='gray',alpha=0.5)
		ax.add_patch(rect)

	"""
	svm分类线
	plt.plot([4.1347719, 4.1347719],[25.64033581, 29.21654402],color="red")
	plt.plot([4.1347719, 4.1347719],[22.06412759, 23.8522317],color="red")
	plt.plot([4.1347719, 4.1347719],[16.69981527, 20.27602349],color="red")

	plt.plot([8.52431189, 8.52431189],[25.64033581, 29.21654402],color="red")
	plt.plot([8.52431189, 8.52431189],[22.06412759, 23.8522317],color="red")
	plt.plot([8.52431189, 8.52431189],[16.69981527, 20.27602349],color="red")

	plt.plot([12.91385188, 12.91385188],[25.64033581, 29.21654402],color="red")
	plt.plot([12.91385188, 12.91385188],[22.06412759, 23.8522317],color="red")
	plt.plot([12.91385188, 12.91385188],[16.69981527, 20.27602349],color="red")

	"""

	plt.show()

def print_all_CDF():
	#文件为knn_err_data.txt， svm_err_data.txt
	f=open("knn_err_data.txt","r")
	knn_data_list = []
	for line in f.readlines():
		knn_data_list.append(float(line))
	print "knn_err_data:", len(knn_data_list), sum(knn_data_list)/len(knn_data_list), " m"
	f.close()
	
	f=open("svm_err_data.txt","r")
	svm_data_list = []
	for line in f.readlines():
		svm_data_list.append(float(line))
	print "svm_err_data:", len(svm_data_list),sum(svm_data_list)/len(svm_data_list), " m"
	f.close()
	
	svm_data_list.sort()
	knn_data_list.sort()
	y_data = []
	for i in range(len(svm_data_list)):
		y_data.append((i+1.0)/len(svm_data_list)*100)
	#plt.title('CDF graph')
	plt.xlabel('Error distance(m)')
	plt.ylabel('percentage(%)')
	plt.plot(knn_data_list,y_data,"--,",label='knn')
	plt.plot(svm_data_list,y_data,"-.,",label='svm')
	plt.legend()
	plt.show()
	
	return
if __name__ == "__main__":
	print "it is test.py!"
	"""
	数据集个数的数据
	x_data = [1,2,4,8,15]
	y_data = [2.38,1.96,1.55,1.21,0.97]
	plt.ylim((0,2.5))
	plt.xlabel('number of train set')
	plt.ylabel('error(m)')
	"""
	"""
	k值
	x_data = [1,3,5,6,9,15]
	y_data = [2.56,2.34,2.41,2.45,2.6,2.85]
	#plt.ylim((0,2.5))
	plt.xlabel('K')
	plt.ylabel('error(m)')
	"""
	"""
	AP选择
	x_data = [448,200,100,80,60,40,20,10,5]
	y_data = [2.34,2.32,2.31,2.30,2.36,2.50,2.42,2.61,2.99]
	#plt.ylim((0,2.5))
	plt.xlabel('number of AP')
	plt.ylabel('error(m)')
	"""
	"""
	write and read
	aa = [2,3,4,1,2]
	f=open("test.txt","w")
	for line in aa:
		f.write(str(line)+'\n')
	f.close()
	f=open("test.txt","r")
	data_list = []
	for line in f.readlines():
		data_list.append(float(line))
	print data_list
	"""
	print_base()
	#print_all_CDF()

	#plt.plot(x_data,y_data)
	#plt.show()
	

