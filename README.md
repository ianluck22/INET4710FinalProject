# INET 4710 Final Project
Parker Erickson, Markus Pettersson, Ian Luck, Prateek Vachher, Tommy Luangrath

# Summary
The purpose of this project is to predict house value using a variety of machine learning methods. Both home buyers and sellers need a reliable metric in order to either determine if a house price is a fair deal. In order for this to happen, images, natural language, and numerical features will all be combined into a machine learning pipeline. The pipeline includes a Convolutional Neural Network for the image data, sentiment analysis on the natural language data, and a neural network for combining the output of these models with the numerical features. We use Mean Absolute Error (MAE) as our evaluator of success. Our system was able to **achieve an MAE of $45,812**. For reference, Zillow’s Zestimate feature has a MAE of $44,800 on the dataset we created. That is a **difference of $1012 (about 2%)** between our method and Zillow’s.

# Data/Downloads
The most comprehensive piece of data was compiled into [dataWithImagePaths.csv](https://github.com/ianluck22/INET4710FinalProject/blob/master/dataWithImagePaths.csv). This includes all data that we scraped from Zillow, as well as the address and selling price obtained throught the Minnesota Department of Revenue. Lastly, it also contains the filepath of each image in our images dataset, which can be downloaded from our Google Drive (too big for Github) [here](https://drive.google.com/file/d/10F8G7rewg5tQtiUyANCITox_9sSOYzS1/view?usp=sharing). If you do not want to train the image regression model, you can also download the pretrained model weights found [here](https://drive.google.com/file/d/10DJ5yYWTLTCyjljsXhJW6a06-weTm6wL/view?usp=sharing).

# Files in Repository
The complete model that combines the NLP and image results with other numerical features can be found [here](https://github.com/ianluck22/INET4710FinalProject/blob/master/DLModels/combined.ipynb). There are multiple notebooks concerning the EDA of our dataset in the [EDA folder](https://github.com/ianluck22/INET4710FinalProject/tree/master/EDA). The image regression model can be found [here](https://github.com/ianluck22/INET4710FinalProject/blob/master/DLModels/zillowCNN.ipynb). The code used to scrape Zillow as well as clean up the Minnesota Department of Revenue database dumps can be found in our [Scraping](https://github.com/ianluck22/INET4710FinalProject/tree/master/Scraping) folder. The datafiles used to keep track of what was already scraped can be found in the [datafiles](https://github.com/ianluck22/INET4710FinalProject/tree/master/datafiles) folder.