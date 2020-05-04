
# coding: utf-8

# In[1]:

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

from PIL import Image
from tqdm import tqdm

import keras
from keras import applications
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras.utils import to_categorical


# In[2]:

df = pd.read_csv("../imageFilenames.csv")


# In[3]:

df = df[df["imgFilepath"] != "no photo"]
df = df[df["totPurchaseAmt"] >= 50000]
df = df[df["totPurchaseAmt"] <= 5000000]
df.drop_duplicates("mediumImageLink", keep = "first", inplace = True)

# df["totPurchaseAmt"] = df["totPurchaseAmt"] / df["totPurchaseAmt"].max()


# In[4]:

IMG_SIZE = 128
imageData = []

for i, row in tqdm(df.iterrows(), total=len(df)):
    try:
        img = Image.open("../"+row["imgFilepath"])
        img = img.resize((IMG_SIZE, IMG_SIZE))
        imageData.append(np.array(img))

    except:
        imageData.append("NONE")
        df.at[i, "imgFilepath"] = "no photo"
        
df["imgData"] = imageData


# In[5]:

df = df[df["imgFilepath"] != "no photo"]

df["amtBucket"] = pd.qcut(df["totPurchaseAmt"], 10)

bucketList = list(df["amtBucket"].unique())
df["amtBucketNum"] = [bucketList.index(i) for i in df["amtBucket"]]


# In[6]:

X = np.array([i for i in np.array(df["imgData"])]).reshape(-1, IMG_SIZE, IMG_SIZE, 3)
y = df["totPurchaseAmt"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# In[7]:

vggModel = Sequential()

vggModel.add(applications.VGG16(weights="imagenet", input_shape=(IMG_SIZE, IMG_SIZE, 3), include_top=False))

numLayers = len(vggModel.layers)

for layer in vggModel.layers[:numLayers-2]:
    layer.trainable = False


vggModel.add(Flatten(input_shape=vggModel.output_shape[1:]))
vggModel.add(Dropout(.1))
vggModel.add(Dense(1, activation="linear"))

vggModel.summary()


# In[8]:

vggModel.compile(loss='mean_absolute_error', optimizer='adam', metrics = ['mae'])


# In[ ]:

vggModel.fit(X_train, y_train, batch_size=32, epochs=200, verbose=1, validation_split=0.1)


# In[ ]:



