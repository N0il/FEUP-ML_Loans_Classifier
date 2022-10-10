# Notas

- datas dos dados -> epoca especifica do pais -> new business understanding
- dados de teste da competição serão posteriores aos dados das tabelas -> melhor usar dados mais recentes para teste? not sure, must check data plots

# Log

## Week 1 - 19/09/2022

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

---

## Week 2 - 26/09/2022

## TODO:
- Data division for evaluation, etc.
- Build first model (eg. Decision Tree - Random Forest)

## Data Splitting and Model Evaluation Methods

### Data Splitting Method

Seeing as our model is meant to predict future loans we choose to divide the data based on a __Time Series__ split.

### Model Evaluation Method

__TODO__

---

## Week 3 - 03/10/2022

## Data Understanding

### Collect Data
Collected data from project assignment

### Describe Data
Data already described in project assignment

### Data exploration
Data analysis that consists on identifying relationships between pairs or small numbers of attributes, results of simple aggregations, properties of significant sub-populations, and simple statistical analyses.

#### Strategies:

- **Univariate analysis**: Univariate analysis is the simplest form of analyzing data. It is only analyzed one specific variable at a time. Some ways you can describe patterns found in univariate data include central tendency (mean, mode and median) and dispersion: range , variance, maximum, minimum, quartiles (including the interquartile range), and standard deviation.

- **Outliers in the data**: These are observations that have relatively large or small values compared to the majority of observations. In order to detect them Boxplot and Cleveland dot plots are two good tools.

- **Homogeneity in variance**: **TODO**

- **Collinearity in covariates**: **TODO**

- **Normally distributed data**: Various statistical techniques assume normality, such as linear regressions and t-tests. Histograms can be used to show data distributions.

- **Missing value in the data**: These type of values make the analysis more complicated. This analysis ca be checking if a particular observation as a zero value, in some cases (e.g. loan amount).

- **Interaction between variables**: Interaction means the relationship of variables will change according to the value of other variables. This type of information can be found by observing the weights of the variables when performing linear regression.

- **Data visualization**: While statistical data exploration methods have specific questions and objectives, data visualization does not necessarily have a specific question. It can just be performed to explore data and get a sense of what the shape of the data is. There are various methods to accomplish this, like, PCA, t-SNE, Perplexity, Cluster size, Topology, Nondeterministic results and UMAP.

So, we start by doing an univariant analisys and check the outliers of the most relevant variables to our business goal.

#### **Loan Status**
- This is by far the most relevant attribute, as it is the one that states if a loan is running well or not and in a sense it is what our model will have to predict.

#### **Loan Amount and Duration**
- Both the loan amount and duration are also of extreme importance in a way that they are intrinsically connected to the difficulty of the loan completion. If the amount is to high for the loanee's monthly income, then it will probably struggle to complete it, or it will just take too much time. Moreover, if the duration is too short and the amount is also high, once again, the loanee will end up on a situation were the monthly installment might be too  high for their income, or available capital.

#### **Loan Duration**
- DOING IT ABOVE

#### **Loan Date**
- TODO

#### **Loan Payments**
- TODO

#### **Client Age**
- TODO

#### **Client Gender**
- TODO

[comment]: # (xico daqui pra baixo)
#### **Client District**
[comment]: # (would make more sense statistics of n of inhabitants/cities/etc per district **District data**)

Statistics metrics | No. of Inhabitants | No. of Cities | Average salary 
---- | ---- | ---- | ---- 
mean | 1.338849e+05 | 6.259740 | 9031.675325
var | 1.874530e+10 | 5.931647 | 624419.748462
std | 1.369135e+05 | 2.435497 | 790.202347
min | 4.282100e+04 | 1.000000 | 8110.000000
25% | 8.585200e+04 | 5.000000 | 8512.000000
median | 1.088710e+05 | 6.000000 | 8814.000000
75% | 1.390120e+05 | 8.000000 | 9317.000000
max | 1.204953e+06 | 11.000000 | 12541.000000
lower limit for outliers | 6.112000e+03 | 0.500000 | 7304.500000
upper limit for outliers | 2.187520e+05 | 12.500000 | 10524.500000
number of lower outliers | 0 | 0 | 0
number of higher outliers | 6 | 0 | 4


#### **Type of Card**
- The type of cards issued have the following distribution

Type of Card | Number of Cards issued
---- | ----
TOTAL | 177
classic | 127
junior | 41
gold | 9

- And here is some data regarding their __issue date__

Metrics | Values
----           | ---- 
mean           | 9.549713e+05
var            | 5.209916e+07
std            | 7.217975e+03
min            | 9.311070e+05
25%            | 9.506160e+05
median         | 9.602210e+05
75%            | 9.608310e+05
max            | 9.612310e+05
lower_limit    | 9.352935e+05
upper_limit    | 9.761535e+05
outliers-      | 1.000000e+00
outliers+      | 0.000000e+00

#### **Balance after transactions**
- TODO

#### **Amount of transactions**
- TODO

#### **Debited amount**
- TODO

#### **Type of transactions**
- TODO

NOTE: review district data, like avg. salary, unemployment rate, n. of crimes


