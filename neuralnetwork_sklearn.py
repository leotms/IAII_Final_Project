# from sklearn.neural_network import MLPClassifier
# from neuralnetwork import *
import pandas as pd
import numpy  as np

def normalize(dataset):
    '''
        Normalizes the data provided in dataset using min-max method.
    '''
    vector_min = []
    vector_max = []

    #this is the normalized version of X
    normalizedDataset = dataset

    n_columns = dataset.shape[1]
    for i in range(0, n_columns - 1):
        m = np.min(dataset[dataset.columns[i]])
        M = np.max(dataset[dataset.columns[i]])
        vector_min.append(m)
        vector_max.append(M)
        normalizedDataset[normalizedDataset.columns[i]]  = np.subtract(normalizedDataset[normalizedDataset.columns[i]], m)
        normalizedDataset[normalizedDataset.columns[i]]  = np.divide(normalizedDataset[normalizedDataset.columns[i]],M - m)

    return normalizedDataset, vector_min, vector_max

def readData(trainset, normalize_set = False):

    dataset = pd.read_csv(trainset, delimiter = ",", index_col = False, usecols=['lenght', 'retweet_count', 'hashtags', 'mentions', 'contains_url', 'demand_words', 'offer_words',  'neg_words', 'pos_words',  'n_known_medicines','cluster'])

    if normalize_set:
        #Normalize Dataset
        dataset, mean, std = normalize(dataset)


    # #fix the dataset as an array of [x1, x2, x3,..., y]
    # aux_dataset = list()
    # for i in range(len(dataset)):
    #     row = dataset.iloc[i]
    #     aux_row = list()
    #     for j in range(len(row)):
    #         aux_row.append(row[j])
    #
    #     aux_dataset.append(aux_row)
    #
    # dataset = aux_dataset
    dataset = dataset.sample(frac=1)
    return dataset

if __name__ == "__main__":

    #loading datasets for E3 part 1
    print("Starting...\nLoading data sets...")
    trainset = readData('data/TrainingSet3.csv', True)
    XTrain = trainset.loc[:, ['lenght','retweet_count', 'hashtags', 'mentions', 'contains_url', 'demand_words', 'offer_words',  'neg_words', 'pos_words',  'n_known_medicines']]
    YTrain = trainset['cluster']
    print(XTrain)

    #load testsets
    testset = readData('data/TestSet3.csv', True)
    XTest = testset.loc[:, ['lenght','retweet_count', 'hashtags', 'mentions', 'contains_url', 'demand_words', 'offer_words',  'neg_words', 'pos_words',  'n_known_medicines']]
    YTest = testset['cluster']
