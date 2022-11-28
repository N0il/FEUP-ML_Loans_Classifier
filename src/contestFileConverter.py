"""This module is an auxiliary tool to convert results
   obtained in the loan classifier to valid kaggle input
"""

import argparse
import sys
import csv

from loadData import loadData

CONTEST_INPUT_DATA_PATH = './../data/input_contest/'


def main(args):
    parser = argparse.ArgumentParser(
                    prog = 'contestFileConverter.py',
                    description = 'This program converts the predictions outputted from the loanClassifiers.py into the kaggle contest format',
                    epilog = 'For more help consult this link: https://www.kaggle.com/competitions/to-loan-or-not-to-loan-that-is-the-question-ac2223/overview/evaluation')

    parser.add_argument('-f', '--predictionsFile', type=str, default='./../data/output/predictions_RandomForestClassifier.csv')

    parsedArgs = parser.parse_args()

    predictionsFile = parsedArgs.predictionsFile

    (_, _, _, _, _, loans, _) = loadData(CONTEST_INPUT_DATA_PATH)

    predictions = []
    ids = []

    # retrieving model predictions for positive class (-1)
    with open(predictionsFile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            predictions.append(row[0]) # -1 1 order

    # retrieving the corresponding loan ids
    for _, row in loans.iterrows():
        ids.append(row['loan_id'])

    if len(ids) != len(predictions):
        print("Error! Loans and predictions lengths don't match\n")

    header = ['Id', 'Predicted']

    # writing results to file
    with open("./../data/output/kagglePredictions.csv","w+", newline="") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerow(header)

        for i in range(len(predictions)):
            csvWriter.writerow([int(ids[i]), predictions[i]])


if __name__ == "__main__":
    main(args=sys.argv[1:])
