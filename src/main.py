import sys
import time
from pipeline import runPipeline

MODEL_TYPES = ['rf']
BOOL_STRINGS = ['true' 'false']

def main(args):
    start_time = time.time()

    if len(args) == 1:
        if args[0].lower() in BOOL_STRINGS and args[1].lower() in BOOL_STRINGS and args[3].lower() in MODEL_TYPES:
            # Parsing arguments
            if args[0] == 'true':
                dataFromFile = True
            dataFromFile = False

            if args[1] == 'true':
                saveCleanData = True
            saveCleanData = False

            modelType = args[3]

            runPipeline(dataFromFile, saveCleanData, 0.25, modelType)
    else:
        print('Usage: main.py [True | False(Default)]\nStates if it runs with data file or generates it in runtime\n')
        runPipeline() # TODO: change this print

    print("\nExecution time: {elapsed:.2f} min".format(elapsed=((time.time() - start_time) / 60)))


if __name__ == "__main__":
    main(args=sys.argv[1:])
