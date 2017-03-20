from neuralnetwork import *

if __name__ == "__main__":

    #loading datasets for E3 part 1
    print("Starting...\nLoading data sets...")
    #load testsets
    testset = readData('data/TestSet.csv', True)

    network = load_network('prueba2.js')

    datasetname = 'Trainset for Neural network'
    print("Predicting using Testset...")
    predictedset, expected_vs_predicted = calculate_predictions(network, testset)
    print("Done.")

    calculate_errors(expected_vs_predicted)
