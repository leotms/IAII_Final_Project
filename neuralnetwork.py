'''
    File:        neuralnetwork.py
    Description: Performs activities related to excercise 2:
                 Creates a neural networks between 2 and 10 neurons in the
                 hidden layer to test 3 pairs of datasets with 500, 1000 and 2000
                 vectors.
    Authors:     Leonardo Martinez #11-10576
                 Nicolas Manan     #06-39883
                 Joel Rivas        #11-10866
    Updated:     03/05/2017
'''

import numpy  as np
import pandas as pd
import json   as js
from   random import random, seed, shuffle
from   math   import exp

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

    dataset = pd.read_csv(trainset, delimiter = ",", index_col = False, usecols=['lenght', 'hashtags', 'mentions', 'contains_url', 'demand_words', 'offer_words',  'neg_words', 'pos_words',  'n_known_medicines','cluster'])

    if normalize_set:
        #Normalize Dataset
        dataset, mean, std = normalize(dataset)


    #fix the dataset as an array of [x1, x2, x3,..., y]
    aux_dataset = list()
    for i in range(len(dataset)):
        row = dataset.iloc[i]
        aux_row = list()
        for j in range(len(row)):
            aux_row.append(row[j])

        aux_dataset.append(aux_row)

    dataset = aux_dataset
    shuffle(dataset)
    return dataset


def init_network(n_inputs, n_hidden, n_outputs):
    '''
        Initializes a neural network with:
            n_inputs:  number of neurons in input layer
            n_hidden:  number of neurons in hidden layer
            n_outputs: number of neurons in output layer
    '''
    network = list()
    #initialize seed
    seed(42)

    #creates neurons for hidden layer
    hidden_layer = list()
    for i in range(n_hidden):
        weights  = list()
        for j in range(n_inputs + 1):
            weights.append(random())
        aux_dict = {'weights': weights}
        hidden_layer.append(aux_dict)

    network.append(hidden_layer)

    #creates neurons for output layer
    outputlayer = list()
    for i in range(n_outputs):
        weights  = list()
        for j in range(n_hidden + 1):
            weights.append(random())
        aux_dict = {'weights': weights}
        outputlayer.append(aux_dict)

    network.append(outputlayer)

    return network

def save_network(network, filename):

    with open(filename, 'w') as fp:
        js.dump(network, fp, indent=4)

    fp.close()

def load_network(filename):
    with open(filename, 'r') as fp:
        network = js.load(fp)

    fp.close
    return network

def activate_neuron(weights, inputs):
    '''
        Activates neuron, meaning it calculates its value given the inputs:
            a = 0(1)*w(1) + ... + 0(n)*w(n)
    '''
    #last weight is the value for the bias neuron
    act_value = weights[-1]
    for i in range(len(weights) - 1):
        act_value += weights[i] * inputs[i]
    return act_value

def sigmoid(act_value):
    '''
        Given a act_value from a neuron, returns the sigmoid value associated.
    '''
    return 1.0/(1.0 + exp(-act_value))

def forward_propagate(network, row):
    '''
        Applies Forward Propagation in the neural network given a row to predict.
    '''
    inputs = row
    for layer in network:
        new_inputs = list()
        for neuron in layer:
            act_value = activate_neuron(neuron['weights'],inputs)
            neuron['output'] = sigmoid(act_value)
            new_inputs.append(neuron['output'])
        inputs = new_inputs
    return inputs

def transfer_derivate(output):
    '''
        Given a output data, calculates its derivate. It is used in backpropagation.
    '''
    return output*(1.0 - output)

def backpropagation(network, expected):
    '''
        Given a neural network and a expected value, applies backpropagation.
        to update delta errors in all neurons.
    '''

    #calculate errors
    for i in reversed(range(len(network))):
        layer = network[i]
        errors = list()

        if i != len(network) - 1:
            #calculate errors for hidden layer
            for j in range(len(layer)):
                error = 0.0
                for neuron in network[i + 1]:
                    error += (neuron['weights'][j] * neuron['delta'])
                errors.append(error)
        else:
            for j in range(len(layer)):
                #calculate errors for output layer.
                neuron = layer[j]
                errors.append(expected[j] - neuron['output'])
        for j in range(len(layer)):
            #Updates delta for all neurons in the network
            neuron = layer[j]
            neuron['delta'] = errors[j] * transfer_derivate(neuron['output'])

def update_weights(network, row, alpha):
    '''
        Given a neural network, the training example(row) and a learning rate (alpha)
        performs an update to all neuron weights in the network, after backpropagation.
    '''
    for i in range(len(network)):
        inputs = row[:-1]
        if i != 0:
            inputs = list()
            for neuron in network[i-1]:
                inputs.append(neuron['output'])
        for neuron in network[i]:
            for j in range(len(inputs)):
                neuron['weights'][j] += alpha*neuron['delta']*inputs[j]
            neuron['weights'][-1] += alpha*neuron['delta']

def train(network, trainset, alpha, n_epoch, n_outputs):
    '''
        Trains a neural network, using a set of training examples.
        performs the training n_epoch times.
        returns a list of iterations vs cost, for future graphics use.
    '''
    iter_vs_cost = [[],[]]

    for epoch in range(n_epoch):
        cost = 0
        for row in trainset:
            output   = forward_propagate(network, row)
            expected = [0 for i in range(n_outputs)]
            expected[int(row[-1])] = 1
            cost += (1/(n_outputs)) * sum([(expected[i] - output[i])**2 for i in range(n_outputs)]) # This calculates the cost function (MSE)
            backpropagation(network, expected)
            update_weights(network, row, alpha)

        iter_vs_cost[0].append(epoch)
        iter_vs_cost[1].append(cost)
        # print('> Epoch=%d, Alpha=%.3f, Cost=%.10f' % (epoch, alpha, cost))

    return iter_vs_cost

def predict(network, row):
    '''
        Predicts a value for a input data in row using Forward Propagation in a given neural network.
        Returns only the value predicted.
    '''
    output = forward_propagate(network, row)
    return output.index(max(output))

def calculate_predictions(network, testset):
    '''
        Preforms predictions over a set of testing examples using Forward Propagation on a given network.
        Returns the predicted set [Xi, X2, ..., Xn, Predicted] and a vector [Expected, Predicted].
        Used for graphics and error calculation respectively.
    '''
    predictedset = list()
    expected_vs_predicted = list()
    for row in testset:
        prediction = predict(network, row)
        expected_vs_predicted.append([row[-1],prediction])
        predictedset.append([row[0],row[1],prediction])

    return predictedset, expected_vs_predicted

def calculate_errors(results):
    '''
        Calculates errors for obtained results.
        Total MSE for Testing.
        # of False Positives
        # of False Negatives
    '''
    total_error     = 0
    false_positives = 0
    false_negatives = 0

    confusion_matrix = []
    for i in range(3):
        confusion_matrix.append([0,0,0])


    #this is the total MSQ for testing
    total_error += (1/len(results)) * sum([(result[0] - result[1])**2 for result in results])


    for result in results:
        #false positive
        for i in range(3):
            for j in range(3):
                if result[0] == i and result[1] == j:
                    confusion_matrix[i][j] += 1

    print(confusion_matrix)

    accuracy = (confusion_matrix[0][0] + confusion_matrix[1][1] + confusion_matrix[2][2])/(len(results))

    recall_0 = confusion_matrix[0][0]/(len(results)/3)
    recall_1 = confusion_matrix[1][1]/(len(results)/3)
    recall_2 = confusion_matrix[2][2]/(len(results)/3)

    precision_0 = confusion_matrix[0][0]/(confusion_matrix[0][0] + confusion_matrix[1][0] + confusion_matrix[2][0])
    precision_1 = confusion_matrix[1][1]/(confusion_matrix[0][1] + confusion_matrix[1][1] + confusion_matrix[2][1])
    precision_2 = confusion_matrix[2][2]/(confusion_matrix[0][2] + confusion_matrix[1][2] + confusion_matrix[2][2])

    print("---- RESULTS ----")
    print("Total MSE: %f"%total_error)
    print('Total Accuracy: %f'%accuracy)
    print('True Positive Rate (recall) for Other Tweets: %f'%recall_0)
    print('True Positive Rate (recall) for Offer Tweets: %f'%recall_1)
    print('True Positive Rate (recall) for Demand Tweets: %f'%recall_2)
    print('Positive Predictive Value (precision) for Other Tweets: %f'%precision_0)
    print('Positive Predictive Value (precision) for Offer Tweets: %f'%precision_1)
    print('Positive Predictive Value (precision) for Demand Tweets: %f'%precision_2)
    return total_error, false_positives, false_negatives
