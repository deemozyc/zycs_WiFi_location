# coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import csv
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpathes

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
#有中文出现的情况，需要u'内容'

from config import *

def list_add(a,b): #两个list的每个数相加
	c = []
	for i in range(len(a)):
		c.append(a[i] + b[i])
	return c
	
def list_max(a,b): #两个list的每个数取max
	c = []
	for i in range(len(a)):
		c.append(max(a[i], b[i]))
	return c
		
def get_kth(a, k): #获得a中第k大的值
	aa = list(a) #为了不改变a
	aa.sort()
	return aa[len(aa)-k]

def AP_choose(a, b, k):
#AP选择 ab向量只保留a的前k大的维度

	scale = get_kth(a, k)
	count = 0
	
	#print "scale:" , scale
	
	mark = [] #第i个元素是否要保留
	for i in a:
		if(i >= scale and count < k):
			mark.append(1)
			count += 1
		else:
			mark.append(0)
	
	#print "mark", mark
	
	new_a = []
	new_b = []
	for i in range(len(a)):
		if(mark[i] == 1):
			new_a.append(a[i])
			new_b.append(b[i])
			
	return [new_a, new_b]
		
	

def get_dis(a, b): #获取两向量的距离 测试集在前
	#先AP选择
	AP = get_AP_limit()
	if(AP < 448):
		[a,b] = AP_choose(a, b, AP)
	
	algorithm = get_distance_algorithm()
	if(algorithm == 'Euclidean_distance'):
		return get_dis_eucl(a, b)
	if(algorithm == 'Manhattan_distance'):
		return get_dis_man(a, b)
	if(algorithm == 'Cosine_distance'):
		return get_dis_cos(a, b)
		
	
def get_dis_eucl(a, b): #欧式距离
	ans = 0
	for i in range(len(a)):
		ans += (a[i] - b[i])**2
	ans = ans**0.5
	return ans

def get_dis_man(a, b): #曼哈顿距离
	ans = 0
	for i in range(len(a)):
		ans += abs(a[i] - b[i])
	return ans


def get_dis_excos(a, b): 
	#去除两向量均无信号的余弦距离 
	temp = a
	temp.sort()
	temp.reverse()
	#scale = temp[5]
	aa = []
	bb = []
	
	for i in range(len(a)):
		if a[i] > scale:
			aa.append(a[i])
			bb.append(b[i])
	#print len(aa)
	ans = np.dot(aa,bb)/(np.linalg.norm(aa)*np.linalg.norm(bb))
	return -ans

def get_dis_cos(a, b): #余弦距离
	return -np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))
	r#eturn get_dis_excos(a, b)
	

def random_color(): #随机颜色
    colorArr = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0,14)]
    return "#" + color
    
def get_csv(filename): #读csv文件为list并转float
	csv_buf = csv.reader(open(filename,'r'))
	csv_list = []
	for i in csv_buf:
		csv_list.append(i)
		
	for i in range(len(csv_list)): #str to float
		csv_list[i] = [ float(x) for x in csv_list[i] ]

	return csv_list
	
def coord_zip(coord): #6个压缩为1个
	ans = []
	for i in range(len(coord)):
		if(i%6 == 0):
			ans.append(coord[i])
	return ans

def rss_nozip(rss): #不压缩，只替换
	#100换-100
	for i in range(len(rss)):
		for j in range(len(rss[i])):
			if rss[i][j] == 100.0:
				rss[i][j] = -100.0
	
	return rss

def rss_zip(rss): #6个平均成1个 可改max等
	#100换-100
	for i in range(len(rss)):
		for j in range(len(rss[i])):
			if rss[i][j] == 100.0:
				rss[i][j] = -100.0
	
	ans = []
	j = 0
	temp = []
	for i in range(len(rss)):
		if(i%6 == 0):
			temp = rss[i]
		else:
			#temp = list_max(temp, rss[i]) #max
			temp = list_add(temp, rss[i]) #avg
		if(i%6 == 5):
			#temp = temp = [ x/1 for x in temp ] #max 可改为0.7
			temp = [ x/6 for x in temp ] #avg
			ans.append(temp)

	return ans
	
def get_shelve_coord(): #获取书架坐标
	filename = "db/shelves.csv"
	csv_buf = csv.reader(open(filename,'r'))
	csv_list = []
	for i in csv_buf:
		csv_list.append(i)
	#print  csv_list
	#去除csv_list的第0行和第0列
	shelve_coord = []
	for i in range(len(csv_list)):
		temp = []
		for j in range(len(csv_list[i])):
			if(i * j != 0): #都不为0
				temp.append(csv_list[i][j])
		if(i != 0):
			shelve_coord.append(temp)
	for i in range(len(shelve_coord)): #str to float
		shelve_coord[i] = [ float(x) for x in shelve_coord[i] ]
	return shelve_coord
	
def print_err(err): #画误差折线图(CDF)
	err.sort()
	x_data = err
	y_data = []
	for i in range(len(err)):
		y_data.append((i+1.0)/len(err)*100)
	plt.title('CDF graph')
	plt.xlabel('Error distance(m)')
	plt.ylabel('percentage(%)')
	plt.plot(x_data,y_data)
	plt.show()
	
def draw_dynamic_pic(std_coord, cal_coord): #动态图
	
	fig,ax = plt.subplots()
	plt.axis([2, 16, 14, 32])
	plt.ion()
	#err_sum = 0
	
	#画书架
	shelve_coord = get_shelve_coord()
	for i in range(0,len(shelve_coord),4): #4个坐标一个书架
		x_min = min(shelve_coord[i][0], shelve_coord[i+1][0], shelve_coord[i+2][0], shelve_coord[i+3][0])
		x_max = max(shelve_coord[i][0], shelve_coord[i+1][0], shelve_coord[i+2][0], shelve_coord[i+3][0])
		y_min = min(shelve_coord[i][1], shelve_coord[i+1][1], shelve_coord[i+2][1], shelve_coord[i+3][1])
		y_max = max(shelve_coord[i][1], shelve_coord[i+1][1], shelve_coord[i+2][1], shelve_coord[i+3][1])
		
		rect = mpathes.Rectangle([x_min, y_min],x_max-x_min, y_max-y_min,color='gray',alpha=0.5)
		ax.add_patch(rect)
	
	for i in range(len(std_coord)):
		temp = random_color()
		plt.scatter(cal_coord[i][0], cal_coord[i][1], c = temp, marker='^',label='calculated coord')
		plt.scatter(std_coord[i][0], std_coord[i][1], c = temp, marker='x', label='real coord')
		#err_sum += get_dis(std_coord[i], cal_coord[i])
		if(i == 0):
			plt.legend()
		plt.pause(1)
	plt.pause(100)
	
def draw_static_pic(std_coord, cal_coord): #静态图
	fig,ax = plt.subplots()
	plt.axis([2, 16, 14, 32])
	#画书架
	shelve_coord = get_shelve_coord()
	for i in range(0,len(shelve_coord),4): #4个坐标一个书架
		x_min = min(shelve_coord[i][0], shelve_coord[i+1][0], shelve_coord[i+2][0], shelve_coord[i+3][0])
		x_max = max(shelve_coord[i][0], shelve_coord[i+1][0], shelve_coord[i+2][0], shelve_coord[i+3][0])
		y_min = min(shelve_coord[i][1], shelve_coord[i+1][1], shelve_coord[i+2][1], shelve_coord[i+3][1])
		y_max = max(shelve_coord[i][1], shelve_coord[i+1][1], shelve_coord[i+2][1], shelve_coord[i+3][1])
		
		rect = mpathes.Rectangle([x_min, y_min],x_max-x_min, y_max-y_min,color='gray',alpha=0.5)
		ax.add_patch(rect)
	
	#plt.ion()
	#err_sum = 0
	for i in range(len(std_coord)):
		temp = random_color()
		plt.scatter(cal_coord[i][0], cal_coord[i][1], c = temp, marker='^',label='calculated coord')
		plt.scatter(std_coord[i][0], std_coord[i][1], c = temp, marker='x', label='real coord')
		#err_sum += get_dis(std_coord[i], cal_coord[i])
		if(i == 0):
			plt.legend()
	plt.show()
		
def deal_rss(rss): #信号预处理
	if(get_rss_algorithm() == 'None'):
		return rss
	if(get_rss_algorithm() == 'DIFF'):
		return rss_diff(rss)
	if(get_rss_algorithm() == 'SSD'):
		return rss_ssd(rss)


def rss_diff(rss): #diff预处理
	ans = []
	for it in rss:
		temp = []
		for i in range(len(it)):
			for j in range(i + 1, len(it)):
				temp.append(it[i] - it[j])
		ans.append(temp)
	return ans
			
def rss_ssd(rss): #ssd预处理
	ans = []
	for it in rss:
		temp = []
		for i in range(len(it) - 1):
				temp.append(it[i + 1] - it[i])
		ans.append(temp)
	return ans

def coord_2d(coord): #3维坐标删除第三维
	for i in coord:
		del(i[2])
	return coord
	

        
if __name__ == "__main__":
	print "this is base.py!"
	print 0.0075/0.4*100.0
	#print print_err([2.1,6.3,4.4,5.2,3.1,7.0])
	
	#[a, b] = AP_choose([5,1,1,5,5],[1,2,3,4,6],3)
	#print a
	#print b

	#print get_kth([3,4,2,5,1],1)
	#print get_dis_cos([1,2,3,4], [5,6,7,8])
	#print rss_diff([[1,2,3,4],[4,5,6,7],[7,8,9,10]])
	#print rss_ssd([[1,2,3,4],[4,5,6,7],[7,8,9,10]])

