# Parametrizzato su funzione 1
import os
import argparse
import json
import random
from itertools import product
from itertools import chain, combinations

# Define all possible values for each parameter

security_header_type_values = [
    "OGS_NAS_SECURITY_HEADER_PLAIN_NAS_MESSAGE",
    "OGS_NAS_SECURITY_HEADER_INTEGRITY_PROTECTED",
    "OGS_NAS_SECURITY_HEADER_INTEGRITY_PROTECTED_AND_NEW_SECURITY_CONTEXT",
    "OGS_NAS_SECURITY_HEADER_INTEGRITY_PROTECTED_AND_PARTICALLY_CIPHTERD",
    "OGS_NAS_SECURITY_HEADER_FOR_SERVICE_REQUEST_MESSAGE",
    "OGS_NAS_SECURITY_HEADER_INTEGRITY_PROTECTED_AND_CIPHTERD_WITH_NEW_INTEGRITY_CONTEXT",
    "OGS_NAS_SECURITY_HEADER_INTEGRITY_PROTECTED_AND_CIPHERED"
]

registration_result_value_values = list(range(-128, 128))
equivalent_plmns_mcc_values = list(range(-128, 128))  # Intero a 8 bit con segno
network_feature_support_ims_values = list(range(-128, 128))  # Intero a 8 bit con segno
pdu_session_status_psi_values = list(range(0, 65536))  # Intero a 16 bit senza segno
pdu_session_reactivation_result_psi_values = list(range(0, 65536))  # Intero a 16 bit senza segno

nssai_values = ["01234567890123456789012345678901234567890123456789012345678901234567890123456789"]
eap_values = ["100"]

def generate_test_case(params_to_include, test_id):
    param_values = {
        "security_header_type": security_header_type_values,
        "registration_result_value": registration_result_value_values,
        "equivalent_plmns_mcc": equivalent_plmns_mcc_values,
        "network_feature_support_ims": network_feature_support_ims_values,
        "pdu_session_status_psi": pdu_session_status_psi_values,
        "pdu_session_reactivation_result_psi": pdu_session_reactivation_result_psi_values,
        "nssai": nssai_values,
        "eap": eap_values
    }

    param_dict = {}

    # Create directory if not exists
    directory_name = "generate_registration_accept_tests"
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

    if args.enable_special_option:
        param_dict["security_header_type"] = "OGS_NAS_SECURITY_HEADER_PLAIN_NAS_MESSAGE"
        param_dict["registration_accept_security"] = "disabled"

    if args.second_function in functions_for_third_row:
        output_data = [
            {"ue_ul_handle": "null", "dl_reply": "null", "command_mode": "null", "dl_params": "null"},
            {"ue_ul_handle": "null", "dl_reply": "null", "command_mode": "null", "dl_params": "null"},
            {"ue_ul_handle": args.second_function, "dl_reply": "registration_accept", "command_mode": "send", "dl_params": param_dict}
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
            {"ue_ul_handle": args.second_function, "dl_reply": "registration_accept", "command_mode": "send", "dl_params": param_dict},
            {"ue_ul_handle": "null", "dl_reply": "null", "command_mode": "null", "dl_params": "null"}
        ]

    output_filename = f'{directory_name}/test_case_{test_id}.json'
    with open(output_filename, 'w') as json_file:
        json.dump(output_data, json_file, indent=2)

#############################################################################################

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1))

def generate_all_possible_test_cases(params_to_include):
    param_values = {
        "security_header_type": security_header_type_values,
        "registration_result_value": registration_result_value_values,
        "equivalent_plmns_mcc": equivalent_plmns_mcc_values,
        "network_feature_support_ims": network_feature_support_ims_values,
        "pdu_session_status_psi": pdu_session_status_psi_values,
        "pdu_session_reactivation_result_psi": pdu_session_reactivation_result_psi_values,
        "nssai": nssai_values,
        "eap": eap_values
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
    parser.add_argument("--num_tests", type=int, help="Number of test cases to generate")
    parser.add_argument('--second_function', type=str, help='Nome della seconda funzione selezionata.')
    parser.add_argument('--seed', type=int, help='The random seed')
    parser.add_argument('--enable_special_option', action='store_true', help='Enable special option for security_header_type')
    parser.add_argument('--use_all_dl_params', action='store_true', help='Use all dl_params selected, ignoring powerset')
    args = parser.parse_args()

    print(f"Received dl_params: {args.dl_params}")
    print(f"Received num_tests: {args.num_tests}")

    if args.enable_special_option and "security_header_type" in args.dl_params:
        args.dl_params.remove("security_header_type")

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
            print(f"Generating {test_id + 1} test cases")
            generate_test_case(selected_params, test_id)