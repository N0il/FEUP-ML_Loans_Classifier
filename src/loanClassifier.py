import argparse
import sys
import time
from pipeline import runPipeline

MODEL_TYPES = ['rf', 'lr', 'dt', 'gb', 'pr', 'svm', 'naive', 'nn']
INPUT_DATA_PATH = './../data/input/'
CREATED_DATA_NAME = 'createdData'

def main(args):
    start_time = time.time()

    parser = argparse.ArgumentParser(
                    prog = 'loanClassifier.py',
                    description = 'This program classifies wether the bank should give or not loans',
                    epilog = 'For more help consult this link: https://github.com/frenato00/ML_2022')

    parser.add_argument('-s', '--trainDataSize', type=float, default=0.75)
    parser.add_argument('-m', '--modelType', type=str, default='rf', choices=MODEL_TYPES)
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-f', '--dataFromFile', action='store_true')
    parser.add_argument('-c', '--saveCleanData', action='store_true')
    parser.add_argument('-b', '--balanceTestData', action='store_true')
    parser.add_argument('-n', '--selectNFeatures', type=int, default=99)
    parser.add_argument('-r', '--randomState', type=int, default=40)
    parser.add_argument('-i', '--inputPath', type=str, default=INPUT_DATA_PATH)
    parser.add_argument('-d', '--createdDataName', type=str, default=CREATED_DATA_NAME)
    parser.add_argument('-t', '--testMode', type=str, default='none') # the file from option <-f> is used as train data and this one as test data

    parsedArgs = parser.parse_args()

    runPipeline(parsedArgs.dataFromFile, parsedArgs.saveCleanData, parsedArgs.trainDataSize, parsedArgs.modelType, parsedArgs.verbose, parsedArgs.balanceTestData, parsedArgs.selectNFeatures, parsedArgs.inputPath, parsedArgs.createdDataName, parsedArgs.randomState, parsedArgs.testMode)

    print("\nExecution time: {elapsed:.2f} min".format(elapsed=((time.time() - start_time) / 60)))


if __name__ == "__main__":
    main(args=sys.argv[1:])
