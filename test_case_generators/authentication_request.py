from ast import arg
import os
import argparse
import json
import random
from itertools import product
from itertools import chain, combinations

# Define all possible values for each parameter
ngksi_tsc_values = ["0", "1", "2", "3", "4", "5", "6", "7", "8" ]
ngksi_ksi_values = ["0", "1", "2", "3", "4", "5", "6", "7", "8" ]
abba_values = ["0000", "1111", "0101", "1010", "2222","9999"]
authentication_parameter_rand_values = ["00000000000000000000000000000000","11111111111111111111111111111111","fd6b00224351b5cdb63d2ed685770862"]
authentication_parameter_autn_values = ["00000000000000000000000000000000","11111111111111111111111111111111","15416fe2889e9000bad3eab473bfcc19"]
eap_message_values = ["0"]

security_header_type_values = [
    "OGS_NAS_SECURITY_HEADER_PLAIN_NAS_MESSAGE",
    "OGS_NAS_SECURITY_HEADER_INTEGRITY_PROTECTED",
    "OGS_NAS_SECURITY_HEADER_INTEGRITY_PROTECTED_AND_NEW_SECURITY_CONTEXT",
    "OGS_NAS_SECURITY_HEADER_INTEGRITY_PROTECTED_AND_PARTICALLY_CIPHTERD",
    "OGS_NAS_SECURITY_HEADER_FOR_SERVICE_REQUEST_MESSAGE",
    "OGS_NAS_SECURITY_HEADER_INTEGRITY_PROTECTED_AND_CIPHTERD_WITH_NEW_INTEGRITY_CONTEXT",
    "OGS_NAS_SECURITY_HEADER_INTEGRITY_PROTECTED_AND_CIPHERED"
]

def generate_test_case(params_to_include, test_id):
    param_values = {
        "ngksi_tsc": ngksi_tsc_values,
        "ngksi_ksi": ngksi_ksi_values,
        "abba": abba_values,
        "authentication_parameter_rand": authentication_parameter_rand_values,
        "authentication_parameter_autn": authentication_parameter_autn_values,
        "eap_message": eap_message_values,
        "security_header_type": security_header_type_values
    }

    param_dict = {}

    # Create directory if not exists
    directory_name = "generate_authentication_request_tests"
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    for param in params_to_include:
        if param in param_values:
            param_dict[param] = random.choice(param_values[param])

    functions_for_third_row = [
            "service_request", 
            "gmm_status", 
            "configuration_update_complete", 
            "deregistration_request", 
            "deregistration_accept"
        ]

    if args.second_function in functions_for_third_row:
        output_data = [
            {"ue_ul_handle": "null", "dl_reply": "null", "command_mode": "null", "dl_params": "null"},
            {"ue_ul_handle": "null", "dl_reply": "null", "command_mode": "null", "dl_params": "null"},
            {"ue_ul_handle": args.second_function, "dl_reply": "authentication_request", "command_mode": "send", "dl_params": param_dict}
        ]
    elif not param_dict:
        output_data = [
            {"ue_ul_handle": "null", "dl_reply": "null", "command_mode": "null", "dl_params": "null"},
            {"ue_ul_handle": "null", "dl_reply": "null", "command_mode": "null", "dl_params": "null"},
            {"ue_ul_handle": args.second_function, "dl_reply": "authentication_request", "command_mode": "send", "dl_params": "null"}
        ]
    else:
        output_data = [
            {"ue_ul_handle": "null", "dl_reply": "null", "command_mode": "null", "dl_params": "null"},
            {"ue_ul_handle": args.second_function, "dl_reply": "authentication_request", "command_mode": "send", "dl_params": param_dict},
            {"ue_ul_handle": "null", "dl_reply": "null", "command_mode": "null", "dl_params": "null"}
        ]

    output_filename = f'{directory_name}/test_case_{test_id}.json'
    with open(output_filename, 'w') as json_file:
        json.dump(output_data, json_file, indent=2)


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1))

def generate_all_possible_test_cases(params_to_include):
    param_values = {
        "ngksi_tsc": ngksi_tsc_values,
        "ngksi_ksi": ngksi_ksi_values,
        "abba": abba_values,
        "authentication_parameter_rand": authentication_parameter_rand_values,
        "authentication_parameter_autn": authentication_parameter_autn_values,
        "eap_message": eap_message_values,
        "security_header_type": security_header_type_values
    }
    
    test_id = 0
    for subset in powerset(params_to_include):
        selected_param_values = [param_values[param] for param in subset]
        for combination in product(*selected_param_values):
            param_dict = dict(zip(subset, combination))
            generate_test_case(param_dict, test_id)
            test_id += 1

    print(f"Generated {test_id} test cases")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Test Cases")
    parser.add_argument("--dl_params", nargs='+', help="List of dl_params to include in test cases", default=[])
    parser.add_argument("--num_tests", type=int, help="Number of test cases to generate", default=1)
    parser.add_argument('--seed', type=int, help='The random seed')
    parser.add_argument('--second_function', type=str, help='Nome della seconda funzione selezionata.')  # Nuova riga
    parser.add_argument('--use_all_dl_params', action='store_true', help='Use all dl_params selected, ignoring powerset')
    args = parser.parse_args()

    print(f"Received dl_params: {args.dl_params}")
    print(f"Received num_tests: {args.num_tests}")

    all_param_combinations = list(powerset(args.dl_params))
    random.shuffle(all_param_combinations)  # mescola l'elenco

    if args.seed is not None:
        random.seed(args.seed)


    if args.use_all_dl_params:
        for test_id in range(args.num_tests):
            print("Using all selected dl_params")
            generate_test_case(args.dl_params, test_id)
    elif args.num_tests is None:
        print("Generating all possible test cases")
        generate_all_possible_test_cases(args.dl_params)
    else:
        for test_id in range(args.num_tests):
            selected_params = random.choice(all_param_combinations)
            print(f"Generating test case with params: {selected_params}")
            generate_test_case(selected_params, test_id)
