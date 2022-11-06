import sys
import time
from pipeline import runPipeline

def main(args):
    start_time = time.time()

    if len(args) == 1:
        if args[0] == 'True' or args[0] == 'False':
            # Parsing arguments
            dataFromFile = args[0]

            runPipeline(dataFromFile, True, 0.25, 'rf')
    else:
        print('Usage: main.py [True | False(Default)]\nStates if it runs with data file or generates it in runtime\n')
        runPipeline()

    print("\nExecution time: %s min" % ((time.time() - start_time) / 60))


if __name__ == "__main__":
    main(args=sys.argv[1:])
