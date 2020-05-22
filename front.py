# coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time
import tkinter as tk
import tkinter.messagebox

import config
from knn_main import *
from svm_main import *
	
def select_svm():
	algorithm_var.set("选择的定位算法：svm算法")
	print("选择了svm算法")
	global algorithm_name
	algorithm_name = "svm"
	#print "algorithm_name:"+algorithm_name
	return

def select_knn():
	algorithm_var.set("选择的定位算法：knn算法")
	print("选择了knn算法")
	global algorithm_name
	algorithm_name = "knn"
	return
	
def select_None():
	predeal_var.set("选择的横向预处理方法：无")
	print("选择了预处理方法：无")
	global predeal_name
	predeal_name = "None"
	return
	
	
def select_SSD():
	predeal_var.set("选择的横向预处理方法：依次差分")
	print("选择了预处理方法：依次差分")
	global predeal_name
	predeal_name = "SSD"
	return
	
def select_DIFF():
	predeal_var.set("选择的横向预处理方法：两两作差")
	print("选择了预处理方法：两两作差")
	global predeal_name
	predeal_name = "DIFF"
	return
	
def select_euclidean():
	dist_var.set("距离计算方式：欧式距离")
	print("选择了欧式距离")
	global dist_name
	dist_name = "Euclidean_distance"
	
	return
	
	
def select_manhattan():
	dist_var.set("距离计算方式：曼哈顿距离")
	print("选择了曼哈顿距离")
	global dist_name
	dist_name = "Manhattan_distance"
	return
	
def select_cosine():
	dist_var.set("距离计算方式：余弦距离")
	print("选择了余弦距离")
	global dist_name
	dist_name = "Cosine_distance"
	return
	
def select_AP(v):
	global AP_number
	AP_number = v
	#print "AP:", AP_nmber
	return

def select_month():
	string = "数据集的月份："+str(month_listbox.get(month_listbox.curselection()))
	month_var.set(string)
	print(string)
	global month_name
	month_name = str(month_listbox.get(month_listbox.curselection()))
	return
	
def select_index():
	string = "选择的测试集："+str(index_listbox.get(index_listbox.curselection()))
	index_var.set(string)
	print(string)
	global index_name
	index_name = str(index_listbox.get(index_listbox.curselection()))
	return
	
def select_dynamic():
	if(dynamic_var.get() == 1):
		print("选择了动态定位图")
	else:
		print("取消选择了动态定位图")
	
	return
	
def select_static():
	if(static_var.get() == 1):
		print("选择了静态定位图")
	else:
		print("取消选择了静态定位图")
	
	return
	
def select_CDF():
	if(CDF_var.get() == 1):
		print("选择了CDF图")
	else:
		print("取消选择了CDF图")
	
	return
	

def knn_test(trn_coord_file, tst_coord_file, trn_rss_file, tst_rss_file):
	#改写knn_main的run_knn_test
	start = time.clock()
	
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
	
	print "knn的平均定位精度误差：", ans_sum/len(tst_rss), " m"
	print "用时：", (time.clock() - start), " s"
	if(CDF_var.get() == 1): #CDF图
		print_err(err)
	if(dynamic_var.get() == 1): #动态图
		draw_dynamic_pic(tst_coord, cal_coord)
	if(static_var.get() == 1): #静态图
		draw_static_pic(tst_coord, cal_coord)
		
	return ans_sum/len(tst_rss)
	
def svm_test(trn_coord_file, tst_coord_file, trn_rss_file, tst_rss_file):
	#改写run_svm_test
	start = time.clock()
	
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
	clf = SVC(probability = True, gamma = 'auto', decision_function_shape='ovo')
	clf.fit(X, Y)
	
	start2 = time.clock() #在线定时
	sum_err = 0
	all_test = 0
	ac_test = 0
	cal_coord = []
	err = []
	for i in range(len(tst_rss)):
		num = clf.predict([tst_rss[i]])
		ans = num2coord(num)
		err.append( get_dis_eucl(ans, tst_coord[i]))
		sum_err += get_dis_eucl(ans, tst_coord[i])
		all_test = all_test + 1
		cal_coord.append(ans)
		#print coord2num(ans), coord2num(tst_coord[i])
		if(coord2num(ans) == coord2num(tst_coord[i])):
			ac_test = ac_test + 1
			
	print "svm的平均定位精度误差：", sum_err/len(tst_rss), " m"
	print "svm的平均分类正确率：", 1.0*ac_test/all_test
	print "用时：", (time.clock() - start), " s，在线用时：", (time.clock() - start2), " s"
	if(CDF_var.get() == 1): #CDF图
		print_err(err)
	if(dynamic_var.get() == 1): #动态图
		draw_dynamic_pic(tst_coord, cal_coord)
	if(static_var.get() == 1): #静态图
		draw_static_pic(tst_coord, cal_coord)
	
	#返回误差和正确率
	return [sum_err/len(tst_rss), 1.0*ac_test/all_test]
	
def final_cal():
	#完整性检测
	if(algorithm_name == ""):
		tkinter.messagebox.showerror(title='WiFi_loctation_front', message='未选择定位算法！') 
		return
	if(predeal_name == ""):
		tkinter.messagebox.showerror(title='WiFi_loctation_front', message='未选择预处理方式！') 
		return
	if(algorithm_name == "knn" and dist_name == ""):
		tkinter.messagebox.showerror(title='WiFi_loctation_front', message='未选择距离计算方式！') 
		return
	if(month_name == ""):
		tkinter.messagebox.showerror(title='WiFi_loctation_front', message='未选择数据集月份！') 
		return
	if(index_name == ""):
		tkinter.messagebox.showerror(title='WiFi_loctation_front', message='未选择测试集！') 
		return

		
	print("开始计算！")
	print("使用的算法："+algorithm_name)
	print("预处理方式："+predeal_name)
	if(algorithm_name == "knn"):
		print("距离计算方式："+dist_name)
		print("AP数目： "+str(AP_number))
	print("数据集月份："+month_name)
	print("选择的测试集："+index_name)
	
	
	#传递计算参数
	if(dist_name != ""):
		config.ex_distance_algorithm(dist_name)
	#print config.get_distance_algorithm()
	config.ex_rss_algorithm(predeal_name)
	#print config.get_rss_algorithm()
	config.ex_AP_limit(int(AP_number))
	#print config.get_AP_limit()
	
	#处理数据集路径
	i = month_name
	j = index_name
	if(int(i) < 10):
		pre = "db/0" + str(i) + "/"
	else:
		pre = "db/" + str(i) + "/"
		
	if(algorithm_name == "knn"):
		temp = knn_test(pre + "trn01crd.csv", pre + "tst0" + str(j) + "crd.csv", pre + "trn01rss.csv", pre + "tst0" + str(j) + "rss.csv")
	else: #svm
		temp = svm_test(pre + "trn01crd.csv", pre + "tst0" + str(j) + "crd.csv", pre + "trn01rss.csv", pre + "tst0" + str(j) + "rss.csv")
	return
	

	
if __name__ == "__main__":

	algorithm_name = ""
	predeal_name = ""
	dist_name = ""
	month_name = ""
	index_name = ""
	AP_number = 448

	window = tk.Tk()
	window.title('WiFi_loctation_front') #窗口名
	window.geometry('400x800')  #尺寸
	
	
	#算法选择
	algorithm_var = tk.StringVar()    # 将label标签的内容设置为字符类型
	algorithm_tip = tk.Label(window, textvariable=algorithm_var, font=('Arial', 12),width=30, height=2)
	algorithm_tip.pack()   #自动调节尺寸的标签
	algorithm_var.set("选择的定位算法：")
	# bg为背景，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高
	svm_button = tk.Button(window, text="svm算法", command = select_svm)
	svm_button.place(x=100, y=50, anchor='nw') #手动调节尺寸的标签
	knn_button = tk.Button(window, text="knn算法", command = select_knn)
	knn_button.place(x=200, y=50, anchor='nw')
	
	#预处理方式选择
	predeal_var = tk.StringVar()   
	predeal_tip = tk.Label(window, textvariable=predeal_var, font=('Arial', 12),width=30, height=2)
	predeal_tip.place(x=50, y=90, anchor='nw')
	predeal_var.set("选择的横向预处理方法：")
	none_button = tk.Button(window, text="无", command = select_None)
	none_button.place(x=100, y=130, anchor='nw') 
	ssd_button = tk.Button(window, text="依次差分", command = select_SSD)
	ssd_button.place(x=153, y=130, anchor='nw')
	diff_button = tk.Button(window, text="两两作差", command = select_DIFF)
	diff_button.place(x=250, y=130, anchor='nw')
	
	#knn的距离选择
	dist_var = tk.StringVar()   
	dist_tip = tk.Label(window, textvariable=dist_var, font=('Arial', 12),width=30, height=2)
	dist_tip.place(x=50, y=170, anchor='nw')
	dist_var.set("距离计算方式（仅用于knn）：")
	euclidean_button = tk.Button(window, text="欧式距离", command = select_euclidean)
	euclidean_button.place(x=63, y=210, anchor='nw') 
	manhattan_button = tk.Button(window, text="曼哈顿距离", command = select_manhattan)
	manhattan_button.place(x=150, y=210, anchor='nw')
	cosine_button = tk.Button(window, text="余弦距离", command = select_cosine)
	cosine_button.place(x=250, y=210, anchor='nw')
	
	#ap选择数
	AP_tip = tk.Label(window, text="选择的AP数目（仅用于knn）：", font=('Arial', 12),width=30, height=2)
	AP_tip.place(x=55, y=250, anchor='nw')

	#ap尺度滑条
	AP_scale = tk.Scale(window,  from_=3, to=448, orient=tk.HORIZONTAL, length=250, resolution=1, command=select_AP)
	AP_scale.set(448)
	AP_number = 448
	AP_scale.place(x=80, y=280, anchor='nw')
	
	#选择的测试数据集
	month_var = tk.StringVar()   
	data_tip = tk.Label(window, textvariable=month_var, font=('Arial', 12),width=15, height=2)
	month_var.set("数据集的月份：")
	data_tip.place(x=55, y=335, anchor='nw')
	
	index_var = tk.StringVar()   
	data_tip = tk.Label(window, textvariable=index_var, font=('Arial', 12),width=15, height=2)
	index_var.set("选择的测试集：")
	data_tip.place(x=220, y=335, anchor='nw')
	
	month_list_var = tk.StringVar()
	month_list_var.set((1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25))
	# 创建Listbox
	month_listbox = tk.Listbox(window, listvariable = month_list_var, width=10, height=8)
	month_listbox.place(x=70, y=375, anchor='nw')
	
	index_list_var = tk.StringVar()
	index_list_var.set((1,2,3,4,5))
	index_listbox = tk.Listbox(window, listvariable = index_list_var, width=10, height=8)
	index_listbox.place(x=230, y=375, anchor='nw')
	
	month_button = tk.Button(window, text="选定月份", command = select_month)
	month_button.place(x=73, y=550, anchor='nw')
	
	index_button = tk.Button(window, text="选定测试集", command = select_index)
	index_button.place(x=233, y=550, anchor='nw')
	
	#输出选项
	output_tip = tk.Label(window, text="选择输出结果：", font=('Arial', 12),width=15, height=2)
	output_tip.place(x=55, y=590, anchor='nw')
	
	dynamic_var = tk.IntVar()
	dynamic_check = tk.Checkbutton(window, text='动态定位图',variable=dynamic_var, onvalue=1, offvalue=0, command=select_dynamic) 
	dynamic_check.place(x=60, y=620, anchor='nw')
	static_var = tk.IntVar()
	static_check = tk.Checkbutton(window, text='静态定位图',variable=static_var, onvalue=1, offvalue=0, command=select_static) 
	static_check.place(x=170, y=620, anchor='nw')
	CDF_var = tk.IntVar()
	static_check = tk.Checkbutton(window, text='CDF图',variable=CDF_var, onvalue=1, offvalue=0, command=select_CDF) 
	static_check.place(x=60, y=650, anchor='nw')
	

	#最终计算按钮
	cal_button = tk.Button(window, text="计算！", command = final_cal, width=10, height=3)
	cal_button.place(x=125, y=700, anchor='nw')
	
	
	#主窗口循环显示
	window.mainloop()
	
	
