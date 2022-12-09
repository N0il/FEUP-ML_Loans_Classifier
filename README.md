# AC 2022
**G_40**:
- Francisco Pires
- Luis Miranda
- Sergio da Gama

# Modules

- These are the developed modules to execute both the predictive and descriptive data mining tasks concerning a bank loaning service.
- To execute this are example commands for windows, but can easily be translated to linux or macOS. Also, it is needed to be in the "src" directory and install all the python dependencies.

## Loans Classifier Usage:

- This is the main module that can be used to process and create data, based on the datasets given. In addition, it can be used to also split the created data into train and test data, training and testing a model with them. Finally, it can be used in "test mode", where it will train a model with a given dataset and test it with a different one, that doesn't have the status column.

- Below there are some examples to interact with the module:

### Create data, saves it to default location, trains and tests with same data (split):
- `python.exe .\loanClassifier.py -m rf -v -b`
- (example for random forest model, balancing data)

### Create data, using custom input data (-i), saves it to custom location (-d), trains and tests with same data (split):
- `python.exe .\loanClassifier.py -m rf -v -b -i ./../data/input_contest/ -d kaggleCreatedData`
- (example for random forest model, balancing data)

### Don't Create data, train model with default data from file and test model with custom data (-t) (test mode):
- `python.exe .\loanClassifier.py -m rf -v -b -n 7 -t ./../data/output/createdKaggleData.csv -f`
- (example for random forest model, balancing data, selecting 7 features)

## Kaggle results converter

- Auxiliary module used to convert the results returned by the main module to the Kaggle competition format.

- `python.exe .\contestFileConverter.py`
- (with default predictions file)

## Clustering

- This module creates clusters with the DBSCAN and K-Means algorithms, using the data created in the main module.

- `python.exe .\clustering.py`
- (uses createdData file)

## Analyse data

- An auxiliary module is used to analyze both the created and the initial data, aiming to improve the main module and our data understanding.

- `python.exe .\analyseData.py`
- (uses createdData file)
