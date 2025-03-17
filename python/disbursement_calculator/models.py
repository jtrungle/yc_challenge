from dataclasses import dataclass
from typing import Annotated
import pandera as pa
import pandas as pd
from pandera.engines.pandas_engine import DateTime, Category, Period
from pandera.typing.pandas import DataFrame

import enum
import warnings


class Disbursements(pa.DataFrameModel):
    sgc_amount: float = pa.Field(ge=0, coerce=True, nullable=False, raise_warning=True)
    payment_made: DateTime = pa.Field(coerce=True, nullable=False)
    pay_period_from: DateTime = pa.Field(coerce=True, nullable=False)
    pay_period_to: DateTime = pa.Field(coerce=True, nullable=False)
    employee_code: str = pa.Field(coerce=True, nullable=False)


class Payslips(pa.DataFrameModel):
    payslip_id: str = pa.Field(coerce=True, nullable=False)
    end: DateTime = pa.Field(coerce=True, nullable=False)
    employee_code: str = pa.Field(coerce=True, nullable=False)
    code: str = pa.Field(coerce=True, nullable=False)
    amount: float = pa.Field(ge=0, coerce=True, nullable=False, raise_warning=True)


class TransformedOutput(pa.DataFrameModel):
    employee_code: str = pa.Field(coerce=True, nullable=False)
    amount: float = pa.Field(coerce=True)
    pay_period_qtr: Annotated[pd.PeriodDtype, "Q"] = pa.Field(nullable=True)
    sgc_amount: float = pa.Field(coerce=True, nullable=True)
    super_payable: float = pa.Field(coerce=True, nullable=True)
    variance: float = pa.Field(coerce=True, nullable=True)


class OteTreament(enum.Enum):
    OTE = "OTE"
    NOT_OTE = "Not OTE"


class PayCodes(pa.DataFrameModel):
    pay_code: str = pa.Field(coerce=True, nullable=False)
    ote_treatment: Category = pa.Field(
        dtype_kwargs={"categories": [x.value for x in OteTreament], "ordered": True},
        nullable=False,
        alias="ote_treament",
        coerce=True,
    )


class SheetNames(enum.Enum):
    DISBURSEMENTS = "Disbursements"
    PAYSLIPS = "Payslips"
    PAY_CODES = "PayCodes"


@dataclass
class PayData:
    payslips: DataFrame[Payslips]
    disbursements: DataFrame[Disbursements]
    pay_codes: DataFrame[PayCodes]


def extract(path: str) -> PayData:
    pay_data = {}
    for sheet_name in list(SheetNames):
        df = pd.read_excel(
            path,
            sheet_name=sheet_name.value,
        )
        if sheet_name == SheetNames.DISBURSEMENTS:
            model = Disbursements
        elif sheet_name == SheetNames.PAYSLIPS:
            model = Payslips
        elif sheet_name == SheetNames.PAY_CODES:
            model = PayCodes
        else:
            raise ValueError("Value not in SheetNames")

        # catch and print warnings
        with warnings.catch_warnings(record=True) as caught_warnings:
            warnings.simplefilter("always")
            validated_df = model.validate(df)
            for warning in caught_warnings:
                print(warning.message)

        pay_data[sheet_name.value] = validated_df

    pay_data = PayData(
        payslips=pay_data[SheetNames.PAYSLIPS.value],
        disbursements=pay_data[SheetNames.DISBURSEMENTS.value],
        pay_codes=pay_data[SheetNames.PAY_CODES.value],
    )

    return pay_data


if __name__ == "__main__":
    path = "/Users/jle/projects/yc_challenge/Sample Super Data.xlsx"
    pay_data = extract(path)
