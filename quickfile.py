import abcs_driver as driver
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("job_id")
parser.add_argument("Provider")
parser.add_argument("Category")
parser.add_argument("CPU")
parser.add_argument("loop_number")

args = parser.parse_args()

for i in range(int(args.loop_number)):
    driver.main(args.job_id, {"CPU":[args.CPU], "Provider":[args.Provider], "Category":[args.Category]})

