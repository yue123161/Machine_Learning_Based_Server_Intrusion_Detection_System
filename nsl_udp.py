from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import *
from k_fold_validation import *
import pickle
import pandas as pd
import numpy as np
model_cat = "udp"
#mapping to mathematical values
class_map = {'normal':0,'anomaly':1}
#reading csv data
csv = pd.read_csv("data/UDP.csv")
columns=["'protocol_type'","'duration'","'src_bytes'","'dst_bytes'","'count'","'srv_count'","'diff_srv_rate'","'dst_host_count'","'dst_host_same_src_port_rate'","'class'"]
df = pd.DataFrame(csv,columns=columns)

#data manipulation, quering required data
df = df.loc[df["'protocol_type'"]=='udp']

df["'class'"].replace(class_map,inplace=True)
print(df)

#slice and dice.
df.pop("'protocol_type'")
label = np.array(df.pop("'class'"))
features = np.array(df)
X_train,X_test,y_train,y_test = train_test_split(features,label,shuffle=True,random_state=77)

#training model
print("Training Model..")
model = RandomForestRegressor()
model.fit(X_train,y_train)

#saving model using pickle
m_name="rfr"
pkl_filename="models/"+model_cat+"_"+m_name+'.pkl'
with open(pkl_filename, 'wb') as file:
    pickle.dump(model, file)

#accuracy calculation
print("Train Accuracy : ", model.score(X_train, y_train))
print("Test Accuracy : ", model.score(X_test, y_test))

#testing data through perdiction
perdict = model.predict([X_test[200]])
print(perdict)
print(y_test[200])

#confusion matrix for reg round
y_pred = model.fit(X_train.round(), y_train.round()).predict(X_test.round())
cnf_matrix = confusion_matrix(y_test.round(), y_pred.round())
print(cnf_matrix)

kf = KFoldValidation()
kf.GetAverageScore(10,features,label,RandomForestRegressor(),X_train)
