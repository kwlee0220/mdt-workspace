import argparse
import re
import json

def extract_defects_from_file(file_path):
    with open(file_path, 'r') as file:
        json_obj = json.loads(file.read())
        # Extract the list of 1s and 0s
        defect_pattern = re.findall(r'[01]', json_obj)
        return [value for value in defect_pattern]

def determine_defect(defect_data):
    """
    defect_data: List of integers where 1 represents a defect and 0 represents a non-defect.
    Returns '1' if any defect (1) is found, otherwise '0'.
    """
    return '1' if any(defect_data) else '0'

if __name__ == '__main__':
    # Argument parsing
    parser = argparse.ArgumentParser(description="Defect Determination and Result Saving")
    parser.add_argument("Defect", type=str, help="Path to first defect data file")
    parser.add_argument("DefectList", type=str, help="Path to second defect data file")
    parser.add_argument("--output", type=str, help="Output file for combined result", required=True)
    args = parser.parse_args()

    # Extract defect data from 'DefectList' file
    defect_list = extract_defects_from_file(args.DefectList)
    print("(Input)  DefectList: ", defect_list)

    # Extract defect data from 'Defect' file
    defect = extract_defects_from_file(args.Defect)
    print("(Input)  Defect: ", defect)

    # Determine if there is a defect
    defect_result = determine_defect(defect)
    print("DefectResult: ", defect_result)

    # Append the defect result to the second file's content
    defect_list.append(defect_result)
    if len(defect_list) > 20:
        defect_list = defect_list[len(defect_list)-20:]
    updated_defect_list = ','.join(defect_list)

    updated_defect_list_json = json.dumps(updated_defect_list)
    print("(Result) Updated DefectList: ", updated_defect_list_json)

    # Output the combined result to the specified output file
    print(f"Saving updated defect list to {args.output}")
    with open(args.output, "w") as out:
        out.write(updated_defect_list_json)
