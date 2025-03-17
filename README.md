# yc_challenge

## setup

Create an environment (optional)

```
python -m venv venv
```

Activate your environment
linux/mac

```
source venv311/bin/activate
```

windows

```
.\venv\Scripts\activate
```

Clone the repo and cd into it

```
pip install .
```

Run the cli

```
python -m disbursement_calculator --file-path /path/to/your/file
```

## Assumptions

- timezone agnostic for now assuming all files follow the same timezone in dates

## Items to flags

Data Validation - outputs from the validation step

- there is a negative payment in a payslip
  - either an employee needed to pay the company back?
  - or there is an error with the dataset
- ote treatment column is misspelt - would flag to client unless its an automated and is consistent on input
- some pay periods in disbursements are overlapping in quarters - if we were to be particular on super earned within a quarter, would need to think about pro-rata or get more data points

Requirements of the task

- requirements for the functions might not satisfy whats expected as it seems to imply some iterative approach to the problem - when it can be solved with data manipulation and in aggregation
