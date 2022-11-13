import argparse
import sys
import time
from pipeline import runPipeline

MODEL_TYPES = ['rf', 'svm', 'naive', 'nn']
BOOL_OPTIONS = ['-f' '-c', '-s', '-m']

def main(args):
    start_time = time.time()

    parser = argparse.ArgumentParser(
                    prog = 'loanClassifier.py',
                    description = 'This program classifies wether the bank should give or not loans',
                    epilog = 'For more help consult this link: https://github.com/frenato00/ML_2022')

    parser.add_argument('-s', '--trainDataSize', type=float, default=0.25)
    parser.add_argument('-m', '--modelType', type=str, default='rf')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-f', '--dataFromFile', action='store_true')
    parser.add_argument('-c', '--saveCleanData', action='store_true')

    parsedArgs = parser.parse_args()

    runPipeline(parsedArgs.dataFromFile, parsedArgs.saveCleanData, parsedArgs.trainDataSize, parsedArgs.modelType, parsedArgs.verbose)

    print("\nExecution time: {elapsed:.2f} min".format(elapsed=((time.time() - start_time) / 60)))


if __name__ == "__main__":
    main(args=sys.argv[1:])
