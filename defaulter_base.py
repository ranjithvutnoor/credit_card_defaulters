# -*- coding: utf-8 -*-
"""defaulter_extension.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PqDU0VJYtYy5OgQXa9fzvzCdqr02zlIe

###importing required libraries
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot

"""### reading data using pandas library"""

data  = pd.read_excel(r'C:\Users\ranji\Dropbox\PC\Desktop\Finannce-Project\credit engine\DEFAULT.xlsx')
data.head()

data.shape

data.describe()

"""### checking any null values present or not. so calling info function"""

data.info()

"""##1.visualization using seaborn library so calling heatmap. 

##2.understanding correlation between the input variables
"""

import matplotlib.pyplot as plt
import seaborn as sns

corr = data.corr()
plt.figure(figsize=(40,30))
sns.heatmap(corr, annot=True, cmap='mako')
plt.title('Correlation Heatmap')
plt.show()

"""##3.here light shades and dark shades indicates the positve correlation and negative correlation between the variables.
##4.color intensity indicates the intensity of realtion between the variables

#preprocessing

###Assinging all variables which are used to predict deafult defined with x
### and the output variable deafult assigned to y
"""

x = data.iloc[:,:-1].values
y = data.iloc[:,-1].values

"""### so x has shaped all rows and 44 columns i.e, except default column """

x.shape

"""###and y shaped with all rows and one column."""

y.shape

"""### printing x and y matrix respectively"""

x

print([y])

y = y.reshape(len(y),1)

print(y)

"""##Now splitting data into 1/4 th for testing data and 3/4 for training data, so called train test split model from sklearn."""

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test1 = train_test_split(x,y,test_size = 0.25,random_state = 0)
x_train,x_test,y_train,y_test2 = train_test_split(x,y,test_size = 0.25,random_state = 0)
x_train,x_test,y_train,y_test3 = train_test_split(x,y,test_size = 0.25,random_state = 0)

"""##Now normalizing data using standard scaler model, so data cannot be biassed from larger values w.r.t smaller digit values."""

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.fit_transform(x_test)

x_train.shape

x_test.shape

"""###normalized values of trained data"""

print(x_train)

y_train.shape

"""##values of y i.e; our output represented in array"""

y

"""# 1. training XG Boost model on the training set so that it will boost performance of training. And yield high accuracy in resulting values."""

from xgboost import XGBClassifier
classifier = XGBClassifier()
classifier.fit(x_train,y_train)

"""##Now training with different classification models.

##1. random forest classifier

#### using ensemble method from random forest, and using no. of trees as 100, and criterion entropy parameters.
"""

from sklearn.ensemble import RandomForestClassifier
classifier1  = RandomForestClassifier(n_estimators = 100, criterion = 'entropy', random_state = 0)
classifier1.fit(x_train,y_train)

"""### from classifier1 objective, I am  calling predict method and prediting using x_test and concatenating both results such as y_test and y_predict in to one matrix with one column. so we can see side by side the output values.

### y_pred, y_test results
"""

y_pred1 = classifier1.predict(x_test)
print(np.concatenate((y_pred1.reshape(len(y_pred1),1), y_test1.reshape(len(y_test1),1)),1))

"""###making confusion matrix using metrix method for y_test and y_pred values"""

from sklearn.metrics import confusion_matrix, accuracy_score
cm1 =  confusion_matrix(y_test1,y_pred1)
print(cm1)

"""###Now calculating accuracy score of the same mentioned above."""

ac1 = accuracy_score(y_test1, y_pred1)*100
ac1

"""##2.Decision tree classifier"""

from sklearn.tree import DecisionTreeClassifier
classifier2 = DecisionTreeClassifier(criterion='entropy', random_state=0)
classifier2 = classifier2.fit(x_train, y_train)

y_pred2 = classifier1.predict(x_test)
print(np.concatenate((y_pred2.reshape(len(y_pred2),1), y_test2.reshape(len(y_test2),1)),1))

"""### y_pred, y_test results"""

y_pred2 = classifier2.predict(x_test)
print(np.concatenate((y_pred2.reshape(len(y_pred2),1), y_test2.reshape(len(y_test2),1)),1))

"""### accuracy score for decision tree"""

from sklearn.metrics import confusion_matrix, accuracy_score
cm2 =  confusion_matrix(y_test2,y_pred2)
print(cm2)

ac2 = accuracy_score(y_test2, y_pred2)*100
ac2

"""#Cross validation model

## Now using cross validation model, and using cross value =10 , so it prepares x_train data into 10 sets and validaitating respectively.
## so the result will be more accurate as we divided train data and tested.
"""

from sklearn.model_selection import cross_val_score
accuracies1 = cross_val_score(classifier1,x_train,y_train,cv =10)
print('accuracy : {:.2f}%'.format(accuracies1.mean()*100))
print('std:{:.3f}%'.format(accuracies1.std()*100))

from sklearn.model_selection import cross_val_score
accuracies2 = cross_val_score(classifier2,x_train,y_train,cv =10)
print('accuracy : {:.2f}%'.format(accuracies2.mean()*100))
print('std:{:.3f}%'.format(accuracies2.std()*100))

"""## 3. using ANN model"""

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
import time

"""###Now fitting ANN model with data

##using add method from sequential to call dense , dropout.
"""

classifier3 = Sequential()

"""### adding drop function to avoid overfitting"""

classifier3.add(Dropout(rate=0.1))

"""###1st hidden layer"""

classifier3.add(Dense(activation="relu", kernel_initializer="uniform", units =10))

"""###2nd hidden layer"""

classifier3.add(Dense(activation="relu", kernel_initializer="uniform", units=10))

"""##output layer

###1.using activation function sigmoid, because it will allows predctions probability in binary


###2.output layer used only units= 1 ,because our output is only binary i.e 0 or 1 
### if output has more than 2 classes we can use no. of output neurons more than 1 
"""

classifier3.add(Dense(activation="sigmoid", kernel_initializer="uniform", units=1))

"""## here we use 3 parameters,
1. here I am using no. of iterations 100.
<br>
<br>
2. using Adam optimizer beacuse it performs stochastic gradient descent, i.e,
<br>
<br>
updates weights, reduce loss function in same batch while predicting.
<br>
<br>
3. here we are predicting binary class so using binary_crossentropy
<br>
<br>
4. here also using accuracy from metrics list

4. using batch_size number is around 32. so it will compare predictions batches in less time.
"""

classifier3.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
classifier3.fit(x_train,y_train, batch_size=10, epochs=100)

"""###predicting from x_test"""

y_pred3 = classifier3.predict(x_test)
y_pred3

y_pred3.shape

"""###Acuuracy score """

accuracy_score(y_test3, np.round(abs(y_pred3)))*100

"""### confusion matrix"""

cm3 = confusion_matrix(y_test3,np.round(abs(y_pred3)))
cm3

"""#Now checking Dominance of classification curves by precision-recall curves"""

from sklearn.metrics import plot_precision_recall_curve

plot_precision_recall_curve(classifier1,x_test,y_test1)

plot_precision_recall_curve(classifier2,x_test,y_test2)

from sklearn.preprocessing import Binarizer
binarizer = Binarizer(threshold = 0.64)
ann_bin =binarizer.fit_transform((y_pred3))
ann_bin

plot_precision_recall_curve(classifier3,x_test,ann_bin)

from sklearn.metrics import classification_report
cr1 =classification_report(y_test1,y_pred1)
np.array((cr1))

from sklearn.metrics import classification_report
cr2 =classification_report(y_test2,y_pred2)
np.array((cr2))

from sklearn.metrics import classification_report
cr3 =classification_report(y_test3,np.round(abs(y_pred3)))
np.array((cr3))

"""#Now plotting roc curve

##$\text{TPR (Sensitivity)} = \frac{TP}{TP + FN}$

##$\text{FPR (1 - Specificity)} = \frac{FP}{TN + FP}$
"""

from sklearn.metrics import roc_curve, roc_auc_score

"""###ROC is the receiver operating characteristic 
###AUROC is the area under the ROC curve

####rf = randomforest,
####dt = decision tree,
####ann=neural network

### calling roc_curve class and creating objects respectively as per given nomenclature for y_test and y_pred for 1,2,3 defined earlier
"""

rf_auc = roc_auc_score(y_test1, y_pred1)
dt_auc = roc_auc_score(y_test2, y_pred2)
ann_auc = roc_auc_score(y_test3, y_pred3)

"""###printing the area under roc curve for given classification, respectively."""

print('Random Forest: AUROC = %.3f' % (rf_auc))
print('Decision Tree: AUROC = %.3f' % (dt_auc))
print('ANN: AUROC = %.3f' % (ann_auc))

"""##Now creating objects for False positives rate and True positive rate for function class roc_curve. respectively for 3 classification models used. """

rf_fpr, rf_tpr, _ = roc_curve(y_test1, y_pred1)
dt_fpr, dt_tpr, _ = roc_curve(y_test2, y_pred2)
ann_fpr, ann_tpr, _ = roc_curve(y_test3, y_pred3)

"""### Plotting roc curve on axis x= false positive rate on x-axis
###                             y= true positive rate on y-axis
### for 3 classifiers rf = random foresrt
###                    dt = decision tree
###                     ann = neural network 
"""

plt.plot(rf_fpr, rf_tpr, marker='.', label='Random Forest (AUROC = %0.3f)' % rf_auc)
plt.plot(dt_fpr, dt_tpr, marker='.', label='Decision Tree (AUROC = %0.3f)' % dt_auc)
plt.plot(ann_fpr, ann_tpr, linestyle='--', label='ANN (AUROC = %0.3f)' % ann_auc)
plt.plot([0,1],[0,1],c='k')# line passes through origin having slope =1, threshold = 0.5

plt.title('ROC Plot')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend() 
plt.show()

"""#Conclusion

###As we see the above plot(graph) contains 3 curves rf,dt,ann.From the curve we can say that,
<br>

###1.for random forest auroc score = 0.616,and Higher the auc score higher will be the power of seperation between classes. 

###2.plotting curve which says the line leans more towards y-axis than any other curve, indicates, by random forest classification the rate of true positive is more, and also this curve has above average false positive rate  which type-1 error not more dangerous than type-2 error.

<br>

###3.This tells 61.6% the model can distinguish between the people who are defaulted or not.

###4. the random forest curve has false positive rate is higher, indicates the people who are elgible for the loan to be sanctioned, but failed to get loan. As they were indicated as default by the model.
"""