from disbursement_calculator.models import (
    OteTreament,
    PayData,
    TransformedOutput,
    extract,
)
from disbursement_calculator.report import ReportGeneration
import pandas as pd
import uuid


class Transformer(object):
    def __init__(self, input_data: PayData, super_rate: float) -> None:
        self.data = input_data
        self.output = None
        self.super_rate = super_rate / 100

    def transform_paycodes(self):
        """handle the misspelt column"""
        self.data.pay_codes.columns = ["pay_codes", "ote_treatment"]

    def transform_disbursements(self):
        """
        create uuid to group by later and an interval index to map to payslips
        and map quarterly period, and group by it
        """
        self.data.disbursements["uuid"] = [
            uuid.uuid4() for x in range(self.data.disbursements.shape[0])
        ]

        self.data.disbursements.index = pd.IntervalIndex.from_arrays(
            self.data.disbursements["pay_period_from"],
            self.data.disbursements["pay_period_to"],
            closed="both",
        )
        self.data.disbursements["pay_period_qtr"] = pd.PeriodIndex(
            self.data.disbursements.pay_period_to, freq="Q"
        )
        self.data.disbursements = (
            self.data.disbursements.groupby(by=["employee_code", "pay_period_qtr"])[
                "sgc_amount"
            ]
            .sum()
            .reset_index()
        )

    def transform_payslips(self):
        self.data.payslips["payslip_qtr"] = pd.PeriodIndex(
            self.data.payslips.end, freq="Q"
        )

    def merge_ote(self, df):
        df = pd.merge(
            df,
            self.data.pay_codes,
            left_on="code",
            right_on="pay_codes",
            how="left",
        )
        return df

    def filter_ote(self, df):
        df = df[df.ote_treatment == OteTreament.OTE.value].copy()
        return df

    def map_disbursement_period(self, df):
        """
        Would consider this solution instead if the datasets were bigger to use sql to join between two dates
        for performance reasons
        https://stackoverflow.com/questions/30627968/merge-pandas-dataframes-where-one-value-is-between-two-others/42796283#42796283
        """

        df["pay_period"] = df["end"].apply(
            lambda x: self.data.disbursements.iloc[
                self.data.disbursements.index.get_loc(x)
            ]["uuid"]
        )
        return df

    def group_by_pay_qtr(self, df):
        df = (
            df.groupby(by=["employee_code", "payslip_qtr"])["amount"]
            .sum()
            .reset_index()
        )
        return df

    def merge_with_disbursement(self, df):
        df = pd.merge(
            df,
            self.data.disbursements,
            left_on=["employee_code", "payslip_qtr"],
            right_on=["employee_code", "pay_period_qtr"],
            how="left",
            suffixes=("", "_y"),
        )
        return df[["employee_code", "amount", "pay_period_qtr", "sgc_amount"]]

    def calculate_super_payable(self, df):
        df["super_payable"] = df["amount"] * self.super_rate
        return df

    def calculate_variance(self, df):
        df["variance"] = df["super_payable"] - df["sgc_amount"]
        return df

    def run(self):
        # some basic transform/prep work
        self.transform_paycodes()
        self.transform_disbursements()
        self.transform_payslips()

        # start with payslip as base
        df = self.data.payslips
        df = self.merge_ote(df)
        df = self.filter_ote(df)
        df = self.group_by_pay_qtr(df)

        df = self.merge_with_disbursement(df)
        df = self.calculate_super_payable(df)
        df = self.calculate_variance(df)
        df = TransformedOutput.validate(df)
        return df
