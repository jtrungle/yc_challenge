import unittest

from disbursement_calculator.models import extract
from disbursement_calculator.report import ReportGeneration
from disbursement_calculator.transform import Transformer
from parameterized import parameterized


# add more cases and results here

FILE_LIST = [
    (
        "sample_data.xlsx",
        9.5,
        [-187.38, 726.97, 178.99, -98.11],
    ),
]


class TestDisbursement(unittest.TestCase):
    """basic test to ensure expected variances are correct upon any code change"""

    @parameterized.expand(FILE_LIST)
    def test_parse_successfully(self, file_path, super_rate, expected_variances):
        pay_data = extract(file_path)
        output_data = Transformer(pay_data, super_rate).run()
        report = ReportGeneration(output_data)
        report.run()
        self.assertEqual(set(expected_variances), set(report.variance_totals))
