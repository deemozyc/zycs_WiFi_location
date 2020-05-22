from sklearn import svm
from sklearn.svm import SVC
import csv
import matplotlib
import matplotlib.pyplot as plt

from base import *

tst_coord = get_csv('db/02/tst01crd.csv')
tst_coord =  coord_zip(tst_coord)

plt.scatter([ i[0] for i in  tst_coord], [i[1] for i in tst_coord])

plt.plot([6,6],[16,30],color="gray")
plt.plot([11,11],[16,30],color="gray")
plt.plot([4,14],[21,21],color="gray")
plt.plot([4,14],[25,25],color="gray")

"""
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

"""
X = [[0,0], [1,1],[2,2],[3,3]]
Y = [3, 2,1,0]
clf = SVC( probability=True)
clf.fit(X,Y)
print(clf.predict([[0,0], [1,1],[2,2],[3,3]]))
print(clf.predict_proba([[0,0], [1,1],[2,2],[3,3]]))
x:[4,14]	y:[16,30]
"""
