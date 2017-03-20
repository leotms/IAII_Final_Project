'''
    File:        excercise3_p1.py
    Description: Performs activities related to excercise 3, part one:
                 Predicts a binary classification for Iris Setosa.
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
    #  - four neurons in the input layer (attributes of examples)
    #  - two neurons in the output layer, since we want to know whether the
    #    example belongs to the Iris Setosa or not.
    n_inputs   = 9
    n_outputs  = 3

    #Neurons range between 2 and 10
    neuron_range = [i for i in range(3,10)]

    #####################################################################
    #                          TRAINSET 50%                             #
    #####################################################################

    for i in range(10):

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

            save_network(network, 'prueba3.js')
