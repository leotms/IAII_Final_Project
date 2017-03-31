'''
    File:        train_neural_network.py
    Description: Creates and trains a newural network whith provided values.
    Authors:     Leonardo Martinez #11-10576
                 Nicolas Manan     #06-39883
                 Joel Rivas        #11-10866
    Updated:     03/05/2017
'''
from neuralnetwork import *

if __name__ == "__main__":

    #using the same learnig rate alpha and epochs
    alpha  = 0.1
    epochs = 150

    #for this problem, we are setting:
    #  - 12 neurons in the input layer (attributes of examples)
    n_inputs   = 12
    n_outputs  = 3

    #Neurons ranges
    neuron_range = [10, 15, 20, 25, 30]

    #####################################################################
    #                          TRAINSET 50%                             #
    #####################################################################

    for i in range(0, 10):

        #loading datasets for E3 part 1
        print("\n\nStarting...\nLoading data sets...")
        trainset = readData('data/TrainingSet_' +str(i)+'.csv', True)
        #load testsets
        testset = readData('data/TestSet_' +str(i)+'.csv', True)

        datasetname = 'Trainset %d for Neural network'%i

        for neurons in neuron_range:
            network = init_network(n_inputs, neurons, n_outputs)

            print("\nTraining %s with %d neurons, %d epochs and alpha = %f..."%(datasetname, neurons, epochs, alpha))
            iter_vs_cost = train(network, trainset, alpha, epochs, n_outputs)
            print("Done.")

            print("Predicting using Trainset...")
            predictedset, expected_vs_predicted = calculate_predictions(network, trainset)
            print("Done.")

            total_error, false_positives, false_negatives = calculate_errors(expected_vs_predicted)

            print("Predicting using Testset...")
            predictedset, expected_vs_predicted = calculate_predictions(network, testset)
            print("Done.")

            total_error, false_positives, false_negatives = calculate_errors(expected_vs_predicted)

            save_network(network, 'NN_N%d_TS%d.js'%(neurons, i))
