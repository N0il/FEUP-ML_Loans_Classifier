from loadData import loadData
from createData import createAgeGroup, createClientGender
from utils import createClientAge

# loading all the csv tables
(accounts, cards, clients, dispositions, districts, loans, transactions) = loadData()

# =============== Feature Creation ===============

# client's gender
genders = createClientGender(clients)

# client's age group
ages = createClientAge(clients)
ageGroups = createAgeGroup(ages)

# client's effort rate result (above 40 -> yes, below 40% -> no)
# TODO

# client's savings rate
# TODO

# client's district average salary
# TODO

# client's district criminality
# TODO

# ================ Combining Data =================
# TODO

# ================ Model Creation =================
# TODO

# ================ Model Testing ==================
# TODO
