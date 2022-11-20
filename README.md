ML 2022:
G_40:
- Francisco Pires
- Luis Miranda
- Sergio da Gama

## Data mining context:

- __Aplication Domain__: Loan Acceptance Prediction.
- __Problem Type__: Prediction.
- __Technical Aspect__: TODO.
- __Tool and Technique__: Python (TODO - add libraries, etc).

## Business understanding:
### Objectives
- __Background__: Bank managers only have a vague idea if a certain client should receive a loan.
- __Business objective__: Improve the bank's lending service by predicting which clients should receive loans.
- __Business Success criteria__: Reduce the percentage of bad loans given by the bank.
### Assess Situation
- __Inventory and Assumptions__: We are working with a given set of data which we assume to be correct.
- __Risk and Contingencies__: may contain outliers in the data. (TODO - To be dealt with in data preparation.)
### Data mining goals
- __Goals__: Predict which clients should receive a loan based on the available data (TODO - complete goal with actually used data)
- __Data Mining Success criteria__: Create predictions on which clients should get loans that as an accuracy of at least 90%.


## Loans Classifier Usage:

### Create data, saves it to default location, trains and tests with same data (split):
- `python.exe .\loanClassifier.py -m rf -v -b`
- (example for random forest model, balancing data)

### Create data, using custom input data (-i), saves it to custom location (-d), trains and tests with same data (split):
- `python.exe .\loanClassifier.py -m rf -v -b -i ./../data/input_contest/ -d kaggleCreatedData`
- (example for random forest model, balancing data)

### Don't Create data, train model with default data from file and test model with custom data (-t) (test mode):
- `python.exe .\loanClassifier.py -m rf -v -b -n 7 -t ./../data/output/createdKaggleData.csv`
- (example for random forest model, balancing data, selecting 7 features)

## Kaggle results converter
- `python.exe .\contestFileConverter.py`
- (with default predictions file)