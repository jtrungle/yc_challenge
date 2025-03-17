# Yellow Canary Code Challenge


## Objective

The task is to take in three pieces of data, payslips for an employee (employee code), payments (disbursements) made to a Super fund and a set of instructions of how to treat each type of payment (Pay Code)

For a company to correctly pay super for an employee they must pay their staff 9.5% of Pay Codes that are treated as Ordinary Time Earnings (OTE) within 28 days after the end of the quarter. Quarters run from Jan-March, Apr-June, Jul-Sept, Oct-Dec.

Super earned between 1st Jan and the 31 st of March (Q1) will need to be paid/Disbursed between the 29th Jan - 28th of Apr.

For example:

Pay Codes are:
	- Salary = OTE
	- Site Allowance = OTE
	- Overtime - Weekend = Not OTE
	- Super Withheld = Not OTE
	
Payslips are:

    Jan 1st Payslip
    	- Code: Salary, Amount $5000
    	- Code: Overtime - Weekend, Amount $1500
    	- Code: Super Withheld = $475

    Feb 1st Payslip
    	- Code: Salary, Amount $5000
    	- Code: Super Withheld = $475

    March 1st Payslip
    	- Code: Salary, Amount $5000
    	- Code: Super Withheld = $475


Disbursements:
- $500 on  27th Feb
- $500 on 30th March
- $500 on 30th Apr

For this Quarter we need to know the following:

	1) Total OTE = $15,000
	2) Total Super Payable = $1425
	3) Total Disbursed = $1000
	4) Variance = $425
	

## Challenge


Create a python-pipeline (a single .py script is acceptable) that reads in the sample file which contains the Disbursements, Payslips and Pay Codes. This should be executed through a CLI. The Pipeline once executed must ask for the filename and path.

The pipeline must include the following:
    1. A function that can calculate what super is payable
    2. A function that determines from when the disbursement is from 
    3. A function that establishes the variance between what was payable and what was disbursed

For Each of the 4 employees show the Quarterly grouping for the OTE amount, Super Payable and the Disbursement totals
