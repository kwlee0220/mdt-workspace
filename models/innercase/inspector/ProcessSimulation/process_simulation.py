import argparse
import re
import random

def extract_defects_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read().strip()
        # Extract the list of 1s and 0s
        defect_pattern = re.findall(r'[01]', content)
        return [int(value) for value in defect_pattern]

def calculate_average_cycle_time(defect_data, cycle_time_per_unit=30, noise_mean=0, noise_std=3):
    """
    defect_data: List of integers where 1 represents a defect and 0 represents a non-defect.
    cycle_time_per_unit: Average cycle time per inspection in seconds (default is 30 seconds).
    noise_mean: Mean of the Gaussian noise added to the average cycle time.
    noise_std: Standard deviation of the Gaussian noise.
    """
    # Calculate total inspection time only for defect cases
    defect_count = sum(defect_data)  # Count of defects
    if defect_count == 0:
        raise ValueError("No defects found in the data.")
    
    total_defect_time = defect_count * cycle_time_per_unit
    average_cycle_time = total_defect_time / defect_count
    
    # Add Gaussian noise to the average cycle time
    noisy_average_cycle_time = average_cycle_time + random.gauss(noise_mean, noise_std)
    
    return noisy_average_cycle_time

if __name__ == '__main__':
    # Argument parsing
    parser = argparse.ArgumentParser(description="Calculate Inspector Average Cycle Time for Defects")
    parser.add_argument("DefectList", type=str, help="Path to defect data file")
    parser.add_argument("--output", type=str, help="Output file for AverageCycleTime result")
    args = parser.parse_args()

    # Extract defect data
    defect_data = extract_defects_from_file(args.DefectList)

    # Calculate average cycle time for defects with Gaussian noise
    average_cycle_time = calculate_average_cycle_time(defect_data)

    # Output result
    if args.output:
        with open(args.output, "w") as out:
            out.write("{}".format(average_cycle_time))
    else:
        print("AverageCycleTime:", average_cycle_time)
