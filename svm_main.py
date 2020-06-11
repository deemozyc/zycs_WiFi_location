# coding:utf-8
from sklearn.svm import SVC
import csv
import time
import matplotlib
import matplotlib.pyplot as plt
from math import ceil, floor

from base import *


def coord2num(coord): #一个坐标转一个序号
	if coord[0] < 6:
		x = 1
	if coord[0] > 6 and coord[0] < 11:
		x = 2
	if coord[0] > 11:
		x = 3
	
	if coord[1] < 21:
		y = 1
	if coord[1] > 21 and coord[1] < 25:
		y = 2
	if coord[1] > 25:
		y = 3
	return x*10 + y

def cal_class(coords): #将坐标构成的list转分类序号构成的list
	ans = []
	for coord in coords:
		ans.append(coord2num(coord))
	return ans

def num2coord( num): #将每组的标号转化为2维坐标（该区域中心的一个整点）
	x=num // 10
	y=num % 10
	ans = []
	if x == 1:
		ans.append(5)
	if x == 2:
		ans.append(9)
	if x == 3:
		ans.append(13)
	if y == 1:
		ans.append(19)
	if y == 2:
		ans.append(23)
	if y == 3:
		ans.append(27)
	
	if(len(ans) != 2):
		print "ERROR!!!!!!!!!!"
		
	return ans

def get_3floor(coord, rss): #只用第3层的数据
	ans_coord = []
	ans_rss = []
	for i in range(len(rss)):
		if(coord[i][2] == 3):
			ans_coord.append(coord[i])
			ans_rss.append(rss[i])
			
	return [ans_coord, ans_rss]
		

def run_svm_test(trn_coord_file, tst_coord_file, trn_rss_file, tst_rss_file): #输入数据集 返回svm的平均误差
	
	trn_coord = get_csv(trn_coord_file)
	trn_coord = coord_zip(trn_coord)

	tst_coord = get_csv(tst_coord_file)
	tst_coord =  coord_zip(tst_coord)
	
	trn_rss = get_csv(trn_rss_file)
	trn_rss = rss_zip(trn_rss)

	tst_rss = get_csv(tst_rss_file)
	tst_rss = rss_zip(tst_rss)
	
	trn_rss = deal_rss(trn_rss)
	tst_rss = deal_rss(tst_rss)
	
	temp = get_3floor(trn_coord, trn_rss)
	trn_coord = temp[0]
	trn_rss = temp[1]
	temp = get_3floor(tst_coord, tst_rss)
	tst_coord = temp[0]
	tst_rss = temp[1]
	
	X = trn_rss
	Y = cal_class(trn_coord)
	clf = SVC(gamma = 'auto', decision_function_shape='ovr', kernel = "poly", C = 2)
	clf.fit(X, Y)
	
	sum_err = 0
	all_test = 0
	ac_test = 0
	err = []
	for i in range(len(tst_rss)):
		num = clf.predict([tst_rss[i]])
		ans = num2coord(num)
		sum_err += get_dis_eucl(ans, tst_coord[i])
		err.append(get_dis_eucl(ans, tst_coord[i]))
		all_test = all_test + 1
		#print coord2num(ans), coord2num(tst_coord[i])
		if(coord2num(ans) == coord2num(tst_coord[i])):
			ac_test = ac_test + 1

	#返回误差和正确率
	return [sum_err/len(tst_rss), 1.0*ac_test/all_test]
	

if __name__ == "__main__":
	
	trn_coord = get_csv('db/01/trn01crd.csv')
	trn_coord = coord_zip(trn_coord)
	
	#trn_coord = coord_2d(trn_coord)
	#print trn_coord[6]

	tst_coord = get_csv('db/01/tst01crd.csv')
	tst_coord =  coord_zip(tst_coord)


	trn_rss = get_csv("db/01/trn01rss.csv")
	trn_rss = rss_zip(trn_rss)


	tst_rss = get_csv("db/01/tst01rss.csv")
	tst_rss = rss_zip(tst_rss)
	
	
	trn_rss = deal_rss(trn_rss)
	tst_rss = deal_rss(tst_rss)


	X = trn_rss
	Y = cal_class(trn_coord)
	#print Y
	clf = SVC(probability = True , gamma = 'auto', decision_function_shape='ovr')
	clf.fit(X, Y)
	
	sum_err = 0
	for i in range(len(tst_rss)):
		num = clf.predict([tst_rss[i]])
		ans = num2coord(num)
		
		sum_err += get_dis_eucl(ans, tst_coord[i])
	
	print sum_err/len(tst_rss)
	
	
	start_time = time.time()
	
	avg_mis = []
	ac_rate = []
	rate_month = []
	mis_month = []
	all_err  =[]
	for i in range(1, 26): #月份
		for j in range(1, 6): #测试集
			if(i < 10):
				pre = "db/0" + str(i) + "/"
			else:
				pre = "db/" + str(i) + "/"
			
			temp = run_svm_test(pre+"trn01crd.csv", pre+"tst0"+str(j)+"crd.csv", pre+"trn01rss.csv", pre+"tst0"+str(j)+"rss.csv")
			print temp
			avg_mis.append(temp[0])
			ac_rate.append(temp[1])
			#all_err.extend(temp[2])
			if(j == 1):
				mis_month.append(temp[0])
				rate_month.append(temp[1])
			else:
				mis_month[-1] = mis_month[-1] + temp[0]
				rate_month[-1] = rate_month[-1] + temp[1]

		mis_month[-1] = mis_month[-1]/5
		rate_month[-1] = rate_month[-1]/5
	
	print "mis_month:", mis_month, sum(mis_month)/25
	print "rate_month:", rate_month, sum(rate_month)/25
	
	print "total_avg = ", sum(avg_mis)/len(avg_mis)
	print "ac_rate = ", sum(ac_rate)/len(ac_rate)*100
	
	print "time: ", (time.time()-start_time), " s"
	
	"""
	print "lem of all_err:",len(all_err)
	f=open("svm_err_data.txt","a")
	for line in all_err:
		f.write(str(line)+'\n')
	f.close()
	"""
	
	
	
	

