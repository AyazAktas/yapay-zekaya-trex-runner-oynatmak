import glob
import os
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import  Conv2D, MaxPooling2D
from PIL import Image
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")

imgs=glob.glob("./img_nihai/*.png")

width=125
height=50

X=[]
Y=[]

for img in imgs:
    filename=os.path.basename(img)
    label=filename.split("_")[0]
    im=np.array(Image.open(img).convert("L").resize((width,height)))
    im=im/255
    X.append(im)
    Y.append(label)

X=np.array(X)
X=X.reshape(X.shape[0],width,height,1)#1 siyah beyaz
def onehot_labels(values):
    label_encoder=LabelEncoder()
    integer_encoded=label_encoder.fit_transform(values)
    onehot_encoder=OneHotEncoder(sparse=False)
    integer_encoded=integer_encoded.reshape(len(integer_encoded),1)
    onehot_encoded=onehot_encoder.fit_transform(integer_encoded)
    return onehot_encoded

Y=onehot_labels(Y)
train_X ,test_X , train_Y , test_Y=train_test_split(X,Y,test_size=0.25,random_state=2)


model=Sequential()
model.add(Conv2D(32,kernel_size=(3,3),activation="relu",input_shape=(width,height,1)))

model.add(Conv2D(64,kernel_size=(3,3),activation="relu"))

model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128,activation="relu"))
model.add(Dropout(0.4))
model.add(Dense(3,activation="softmax"))

model.compile(loss="categorical_crossentropy",optimizer="Adam",metrics=["accuracy"])
model.fit(train_X,train_Y,epochs=70,batch_size=20)

score_train=model.evaluate(train_X,train_Y)
print("Eğitim Doğruluğu: %",score_train[1]*100)

score_test=model.evaluate(test_X,test_Y)
print("Test Doğruluğu: %",score_test[1]*100)

# Modeli JSON dosyasına kaydetmek
with open("model_new.json", "w") as json_file:
    json_file.write(model.to_json())

# Model ağırlıklarını kaydetmek
model.save_weights("trex_weight.h5")
