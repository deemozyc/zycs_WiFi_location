# zycs_WiFi_location  
A simple Fingerprint positioning system with svm and knn   
requirements:Python2, sklearn, matplotlib  
data from:Mendoza Silva, German & Richter, Philipp & Torres-Sospedra, Joaquín & Lohan, Elena Simona & Huerta, Joaquín. (2018). Long-Term WiFi Fingerprinting Dataset for Research on Robust Indoor Positioning. Data. 3. 3. 10.3390/data3010003.  
  
base.py：包括WiFi信号预处理函数，绘图函数等基础函数，无具体算法的函数。无须直接执行本代码。  
check.py：验证是否所有数据都是采集6次的，确实都是。  
config.py：配置knn算法的3个参数文件，有读写这3个参数的函数。  
knn_main.py：knn算法的代码。直接执行会进行大数据测试，run_knn_test()函数执行单组测试。  
svm_main.py：svm算法的代码。直接执行会进行大数据测试，run_svm_test()函数执行单组测试。  
get_floor.py：两种算法楼层检测的代码，修改了run_knn_test()和run_svm_test()的代码，复用了基础代码。  
front.py：前端界面的代码，是上述代码功能的子集，只能执行单组测试，但有界面。  
plot.py：记录结果，画图的代码，比较简单。  
test.py：画地图用的代码，比较简单。    
运行前需要将数据集中的db文件夹放与代码文件放在同一目录下，或直接更改代码中数据集的路径。
