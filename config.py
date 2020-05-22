# coding:utf-8
distance_algorithm = 'Euclidean_distance' 
"""
knn距离算法设置，误差计算固定用欧氏距离，knn中的距离可选，可选：
Euclidean_distance(欧氏距离)
Manhattan_distance(曼哈顿距离)
Cosine_distance(余弦距离)
"""

rss_algorithm = 'None'
"""
rss处理方法
None(不处理) N
DIFF(两两做差) N*（N-1）
SSD(相邻的做差) N-1
"""

AP_limit = 448
"""
knn计算距离时的AP选择数量，默认448（全部AP）
"""

def get_distance_algorithm():
	return distance_algorithm
	
def ex_distance_algorithm(new_distance_algorithm):
	if(new_distance_algorithm != "Euclidean_distance" and new_distance_algorithm != "Manhattan_distance" and new_distance_algorithm != "Cosine_distance"):
		print "错误的距离定义！修改失败"
		return
	global distance_algorithm
	distance_algorithm = new_distance_algorithm
	
def get_rss_algorithm():
	return rss_algorithm

def ex_rss_algorithm(new_rss_algorithm):
	if(new_rss_algorithm != "None" and new_rss_algorithm != "DIFF" and new_rss_algorithm != "SSD"):
		print "错误的预处理方式！修改失败"
		return
	global rss_algorithm
	rss_algorithm = new_rss_algorithm

def get_AP_limit():
	return AP_limit
	
def ex_AP_limit(new_AP_limit):
	#print "new_AP_limit:", new_AP_limit, type(new_AP_limit)
	if(new_AP_limit < 1 or new_AP_limit > 448):
		print "不合法的AP数！修改失败"
		return
	global AP_limit
	AP_limit = new_AP_limit
	
if __name__ == "__main__":
	print "it's config.py!!"
	#ex_AP_limit(12)

