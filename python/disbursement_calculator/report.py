from tabulate import tabulate
from typing import Optional
from pandera.typing.pandas import DataFrame

from disbursement_calculator.models import TransformedOutput


class ReportGeneration(object):
    def __init__(self, output: DataFrame[TransformedOutput]) -> None:
        self.output_data = output
        self.reports: Optional[list[DataFrame[TransformedOutput]]] = None
        self.variance_totals: Optional[list[float]] = None

    @staticmethod
    def add_totals(df):
        df.loc["Column_Total"] = df.sum(numeric_only=True, axis=0)
        return df

    def run(self):
        self.reports = []
        self.variance_totals = []
        df = self.output_data
        for employee in df.employee_code.unique():
            employee_df = df[df.employee_code == employee].reset_index(drop=True)
            employee_df = employee_df.sort_values(by="pay_period_qtr")
            employee_df = self.add_totals(employee_df)
            employee_df = employee_df.round(2)
            self.reports.append(employee_df)
            total_variance = employee_df.variance.iloc[-1]
            self.variance_totals.append(total_variance)

    def print(self):
        if not self.reports:
            raise ValueError("No reports found - have you run the report generation?")

        for report in self.reports:
            print(
                tabulate(report, headers="keys", tablefmt="psql", disable_numparse=True)
            )
