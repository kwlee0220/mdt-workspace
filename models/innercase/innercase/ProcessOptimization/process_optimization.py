import argparse
import os
import re
import random

def extract_float_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        
        # Find the first value that matches the floating-point pattern
        match = re.search(r'[-+]?\d*\.\d+|\d+', content)
        
        if match:
            return float(match.group())
        else:
            raise ValueError("No floating-point value found in the file.")

def simulate_production(cycle_times, total_time=8 * 3600, noise_mean=0, noise_std=10):
    """
    cycle_times: List of cycle times for each process (in seconds)
    total_time: Total time for simulation (in seconds), default is 8 hours (28800 seconds)
    noise_mean: Mean of the Gaussian noise added to the production count
    noise_std: Standard deviation of the Gaussian noise
    """
    # Select the cycle time of the process with the longest time (production rate based on bottleneck)
    bottleneck_cycle_time = max(cycle_times)
    
    # Calculate total possible production quantity
    production_count = total_time // bottleneck_cycle_time
    
    # Add Gaussian noise
    noisy_production_count = production_count + random.gauss(noise_mean, noise_std)
    
    # Ensure the production count remains an integer
    return int(noisy_production_count)

if __name__ == '__main__':
    # Argument parsing
    parser = argparse.ArgumentParser(description="RNN-based Fault detection (Long-term)")
    parser.add_argument("HTCycleTime", type=str, help="path for HeaterCycletime")
    parser.add_argument("VFCycleTime", type=str, help="path for FormerCycletime")
    parser.add_argument("PTCycleTime", type=str, help="path for TrimmerCycletime")
    parser.add_argument("QICycleTime", type=str, help="path for InspectorCycletime")
    parser.add_argument("--output", type=str, help="TotalThroughput output file")
    args = parser.parse_args()

    # Read cycle time for each process from file
    heaterCycletime = extract_float_from_file(args.HTCycleTime)
    formerCycletime = extract_float_from_file(args.VFCycleTime)
    trimmerCycletime = extract_float_from_file(args.PTCycleTime)
    inspectorCycletime = extract_float_from_file(args.QICycleTime)

    # Simulation 
    cycle_times = [heaterCycletime, formerCycletime, trimmerCycletime, inspectorCycletime]
    totalThroughput = simulate_production(cycle_times)

    # Print result
    if args.output:
        with open(args.output, "w") as out:
            out.write("{}".format(totalThroughput))
    else:
        print("Total Throughput:", totalThroughput)
