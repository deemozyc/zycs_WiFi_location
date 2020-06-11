# coding:utf-8
import csv
import time
import matplotlib
import matplotlib.pyplot as plt

from base import *

def dis_sort(tst, trn): #返回排序后的【距离，序号】的list
	dis = []
	count = 0
	#print len(trn)
	for i in trn:
		#print "tst", len(tst)
		dis.append([get_dis(tst, i), count])
		count = count + 1
	dis.sort()
	return dis

		
def get_knn(nn_list, trn_coord): #计算knn结果
	
	#k = 30
	#k = 15
	#k = 9 
	#k = 6 
	#k = 5
	k = 3 
	#k = 1 
	"""
	#根据阈值，效果不佳
	thr = 70
	k = 3
	for i in range(len(nn_list) - 1):
		k = max(i, k)
		if(nn_list[i + 1][0] > thr):
			break
	"""
	weight = 0
	wei_sum = 0
	ans = [0, 0, 0]
	for i in range(k):
		weight = 1/(nn_list[i][0]+1e-6) #1e-6防止除以0
		wei_sum = wei_sum + weight
		ans = list_add(ans, [x*weight for x in trn_coord[nn_list[i][1]] ])
	ans = [x/wei_sum for x in ans]
	return ans

def run_knn_test(trn_coord_file, tst_coord_file, trn_rss_file, tst_rss_file):
	#输入数据集 返回knn的平均误差
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
	ans_sum = 0
	cal_coord = []
	err = []
	for i in range(len(tst_rss)):
		nn_list = dis_sort(tst_rss[i], trn_rss)
		ans = get_knn(nn_list, trn_coord)
		cal_coord.append(ans)
		err.append(get_dis_eucl(ans, tst_coord[i]))
		ans_sum = get_dis_eucl(ans, tst_coord[i]) + ans_sum
	#return ans_sum/len(tst_rss)
	return ans_sum/len(tst_rss)
	
if __name__ == "__main__":
	

	"""
	trn_coord = []
	for i in range(9):
		if(i == 0):
			continue
		if(i<10):
			filename = 'db/01/trn0' + str(i) + 'crd.csv'
		else:
			filename = 'db/01/trn' + str(i) + 'crd.csv'
		temp = get_csv(filename)
		temp = coord_zip(temp)
		trn_coord += temp
	
	
	#trn_coord = get_csv('db/01/trn01crd.csv')
	#trn_coord = coord_zip(trn_coord)

	tst_coord = get_csv('db/01/tst01crd.csv')
	tst_coord =  coord_zip(tst_coord)


	
	
	trn_rss = []
	for i in range(9):
		if(i == 0):
			continue
		if(i<10):
			filename = 'db/01/trn0' + str(i) + 'rss.csv'
		else:
			filename = 'db/01/trn' + str(i) + 'rss.csv'
		temp = get_csv(filename)
		temp = rss_zip(temp)
		trn_rss += temp
	
	#trn_rss = get_csv("db/01/trn01rss.csv")
	#trn_rss = rss_zip(trn_rss)


	tst_rss = get_csv("db/01/tst01rss.csv")
	tst_rss = rss_zip(tst_rss)
	
	
	trn_rss = deal_rss(trn_rss)
	tst_rss = deal_rss(tst_rss)
	
	
	ans_sum = 0
	cal_coord = []
	err = []
	for i in range(len(tst_rss)):
		nn_list = dis_sort(tst_rss[i], trn_rss)
		ans = get_knn(nn_list, trn_coord)
		cal_coord.append(ans)
		err.append(get_dis_eucl(ans, tst_coord[i]))
		ans_sum = get_dis_eucl(ans, tst_coord[i]) + ans_sum
	print "avg_error:", ans_sum/len(tst_rss)
	"""
	
	start_time = time.time()
	
	ans = []
	month = []
	all_err  =[]
	for i in range(1, 26): #月份
		for j in range(1, 6): #测试集
			if(i < 10):
				pre = "db/0" + str(i) + "/"
			else:
				pre = "db/" + str(i) + "/"
			
			temp = run_knn_test(pre + "trn01crd.csv", pre + "tst0" + str(j) + "crd.csv", pre + "trn01rss.csv", pre + "tst0" + str(j) + "rss.csv")
			#all_err.extend(temp_err)
			print temp
			ans.append(temp)
			if(j == 1):
				month.append(temp)
			else:
				month[-1] = month[-1] + temp
		month[-1] = month[-1]/5
	print month, sum(month)/25
	print "total_avg = ", sum(ans)/len(ans)
	
	print "time: ", (time.time()-start_time), " s"
	
	"""
	写入文件用
	print "lem of all_err:",len(all_err)
	
	f=open("knn_err_data.txt","w")
	for line in all_err:
		f.write(str(line)+'\n')
	f.close()
	"""
	#print run_test("db/01/trn01crd.csv", "db/01/tst01crd.csv", "db/01/trn01rss.csv", "db/01/tst01rss.csv")
	#print_err(err)
		
	#draw_dynamic_pic(tst_coord, cal_coord)

