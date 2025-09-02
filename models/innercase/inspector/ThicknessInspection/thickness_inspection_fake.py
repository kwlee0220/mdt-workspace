import argparse
import re
import random

def generate_defect_string():
    values = []
    for _ in range(9):
        # Generate 0 with 95% probability and 1 with 5% probability
        if random.random() < 0.05:
            values.append(1)
        else:
            values.append(0)
    # Convert list to a comma-separated string
    return ",".join(map(str, values))

if __name__ == '__main__':
    # Argument parsing
    parser = argparse.ArgumentParser(description="Calculate Inspector Average Cycle Time for Defects")
    parser.add_argument("UpperIlluminanceImage", type=str, help="Upper Illuminance Image path")
    parser.add_argument("--output", type=str, help="Output file for Defect result")
    args = parser.parse_args()


    # Calculate 
    defect_string = generate_defect_string()
    print("Defect:", defect_string)

    # Output result
    if args.output:
        with open(args.output, "w") as out:
            out.write(defect_string)
        
