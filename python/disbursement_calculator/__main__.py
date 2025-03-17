import argparse
import logging
import warnings
import os

from disbursement_calculator.models import extract
from disbursement_calculator.report import ReportGeneration
from disbursement_calculator.transform import Transformer


logging.basicConfig(level=logging.INFO)


def restricted_float(x):
    try:
        x = float(x)
    except ValueError:
        raise argparse.ArgumentTypeError("%r not a floating-point literal" % (x,))

    if x < 0.0 or x > 100.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 100.0]" % (x,))
    return x


def parse_args():
    parser = argparse.ArgumentParser("Tool to calculate correct super disbursement")
    parser.add_argument(
        "--file-path",
        help="Provide path of folder containing the files",
    )

    parser.add_argument(
        "--super-rate",
        help="Provide super rate - 9.5 for 9.5%",
        default=9.5,
        type=restricted_float,
    )
    return parser.parse_args()


def main(args):
    warnings.simplefilter(action="ignore", category=FutureWarning)

    pay_data = extract(args.file_path)
    output_data = Transformer(pay_data, args.super_rate).run()
    report = ReportGeneration(output_data)
    report.run()
    report.print()


if __name__ == "__main__":
    args = parse_args()
    main(args)
