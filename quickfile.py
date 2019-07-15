import abcs_driver as driver
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("job_id")
parser.add_argument("Provider")
parser.add_argument("Category")
parser.add_argument("CPU")

args = parser.parse_args()

driver.main(args.job_id, {"CPU":[args.CPU], "Provider":[args.Provider], "Category":[args.Category]})

