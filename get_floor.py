# coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from knn_main import *
from sklearn.svm import SVC
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

def run_knn_floor(trn_coord_file, tst_coord_file, trn_rss_file, tst_rss_file):
	#与run_knn_test类似 返回楼层测试正确率
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
		floor = round(ans[2])
		#print floor, trn_coord[i][2]
		if(abs(floor - tst_coord[i][2])<1e-6):
			ans_sum = ans_sum + 1
		#else:
			#print ans[2],floor, tst_coord[i][2]
	return 1.0*ans_sum/len(tst_rss)
	
def cal_class(coords):
	#返回楼层 
	ans = []
	for coord in coords:
		ans.append(coord[2])
	return ans
	
	
	return
	
def run_svm_floor(trn_coord_file, tst_coord_file, trn_rss_file, tst_rss_file):
	#与run_knn_test类似 返回楼层测试正确率
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

	
	X = trn_rss
	Y = cal_class(trn_coord)

	#clf = SVC(probability = True, gamma = 'auto')
	clf = SVC(gamma = 'auto', kernel = "poly", C = 2)
	clf.fit(X, Y)
	
	ac_test = 0
	for i in range(len(tst_rss)):
		floor = clf.predict([tst_rss[i]])

		if(abs(floor[0] - tst_coord[i][2]) < 1e-6):
			ac_test = ac_test + 1
		#else:
			#print floor[0], tst_coord[i][2]

	return 1.0*ac_test/len(tst_rss)
	
	
if __name__ == "__main__":
	ans = []
	month = []
	for i in range(1, 26): #月份
		for j in range(1, 6): #测试集
			if(i < 10):
				pre = "db/0" + str(i) + "/"
			else:
				pre = "db/" + str(i) + "/"
			
			#temp = run_knn_floor(pre + "trn01crd.csv", pre + "tst0" + str(j) + "crd.csv", pre + "trn01rss.csv", pre + "tst0" + str(j) + "rss.csv")
			temp = run_svm_floor(pre + "trn01crd.csv", pre + "tst0" + str(j) + "crd.csv", pre + "trn01rss.csv", pre + "tst0" + str(j) + "rss.csv")
			print temp
			ans.append(temp)
			if(j == 1):
				month.append(temp)
			else:
				month[-1] = month[-1] + temp
		month[-1] = month[-1]/5
	print "month:", month
	
	print "total_avg = ", sum(ans)/len(ans)
	
