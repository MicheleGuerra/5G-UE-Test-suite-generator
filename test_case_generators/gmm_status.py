# Parametrizzato su funzione 1
import os
import argparse
import json
import random
from itertools import product
from itertools import chain, combinations

# Define all possible values for each parameter
gmm_cause_values = [
    "OGS_5GMM_CAUSE_ILLEGAL_UE",
    "OGS_5GMM_CAUSE_ILLEGAL_ME",
    "OGS_5GMM_CAUSE_UE_IDENTITY_CANNOT_BE_DERIVED_BY_THE_NETWORK",
    "OGS_5GMM_CAUSE_IMPLICITLY_DE_REGISTERED",
    "OGS_5GMM_CAUSE_PEI_NOT_ACCEPTED",
    "OGS_5GMM_CAUSE_5GS_SERVICES_NOT_ALLOWED",
    "OGS_5GMM_CAUSE_PLMN_NOT_ALLOWED",
    "OGS_5GMM_CAUSE_TRACKING_AREA_NOT_ALLOWED",
    "OGS_5GMM_CAUSE_ROAMING_NOT_ALLOWED_IN_THIS_TRACKING_AREA",
    "OGS_5GMM_CAUSE_NO_SUITABLE_CELLS_IN_TRACKING_AREA",
    "OGS_5GMM_CAUSE_N1_MODE_NOT_ALLOWED",
    "OGS_5GMM_CAUSE_REDIRECTION_TO_EPC_REQUIRED",
    "OGS_5GMM_CAUSE_NON_3GPP_ACCESS_TO_5GCN_NOT_ALLOWED",
    "OGS_5GMM_CAUSE_TEMPORARILY_NOT_AUTHORIZED_FOR_THIS_SNPN",
    "OGS_5GMM_CAUSE_PERMANENTLY_NOT_AUTHORIZED_FOR_THIS_SNPN",
    "OGS_5GMM_CAUSE_NOT_AUTHORIZED_FOR_THIS_CAG_OR_AUITHORIZED_FOR_CAG_CELLS_ONLY",
    "WIRELESS_ACCESS_AREA_NOT_ALLOWED",
    "OGS_5GMM_CAUSE_MAC_FAILURE",
    "OGS_5GMM_CAUSE_SYNCH_FAILURE",
    "OGS_5GMM_CAUSE_CONGESTION",
    "OGS_5GMM_CAUSE_UE_SECURITY_CAPABILITIES_MISMATCH",
    "OGS_5GMM_CAUSE_SECURITY_MODE_REJECTED_UNSPECIFIED",
    "OGS_5GMM_CAUSE_NON_5G_AUTHENTICATION_UNACCEPTABLE",
    "OGS_5GMM_CAUSE_RESTRICTED_SERVICE_AREA",
    "OGS_5GMM_CAUSE_LADN_NOT_AVAILABLE",
    "OGS_5GMM_CAUSE_NO_NETWORK_SLICES_AVAILABLE",
    "OGS_5GMM_CAUSE_MAXIMUM_NUMBER_OF_PDU_SESSIONS_REACHED",
    "OGS_5GMM_CAUSE_INSUFFICIENT_RESOURCES_FOR_SPECIFIC_SLICE_AND_DNN",
    "OGS_5GMM_CAUSE_INSUFFICIENT_RESOURCES_FOR_SPECIFIC_SLICE",
    "OGS_5GMM_CAUSE_NGKSI_ALREADY_IN_USE",
    "OGS_5GMM_CAUSE_SERVING_NETWORK_NOT_AUTHORIZED",
    "OGS_5GMM_CAUSE_PAYLOAD_WAS_NOT_FORWARDED",
    "OGS_5GMM_CAUSE_DNN_NOT_SUPPORTED_OR_NOT_SUBSCRIBED_IN_THE_SLICE",
    "OGS_5GMM_CAUSE_INSUFFICIENT_USER_PLANE_RESOURCES_FOR_THE_PDU_SESSION",
    "OGS_5GMM_CAUSE_SEMANTICALLY_INCORRECT_MESSAGE",
    "OGS_5GMM_CAUSE_INVALID_MANDATORY_INFORMATION",
    "OGS_5GMM_CAUSE_MESSAGE_TYPE_NON_EXISTENT_OR_NOT_IMPLEMENTED",
    "OGS_5GMM_CAUSE_MESSAGE_TYPE_NOT_COMPATIBLE_WITH_THE_PROTOCOL_STATE",
    "OGS_5GMM_CAUSE_INFORMATION_ELEMENT_NON_EXISTENT_OR_NOT_IMPLEMENTED",
    "OGS_5GMM_CAUSE_CONDITIONAL_IE_ERROR",
    "OGS_5GMM_CAUSE_MESSAGE_NOT_COMPATIBLE_WITH_THE_PROTOCOL_STATE"
]

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
        "gmm_cause": gmm_cause_values,
        "security_header_type": security_header_type_values
    }

    param_dict = {}

    # Create directory if not exists
    directory_name = "generate_send_gmm_status_tests"
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
        param_dict["gmm_status_security"] = "disabled"

    if args.second_function in functions_for_third_row:
        output_data = [
            {"ue_ul_handle": "null", "dl_reply": "null", "command_mode": "null", "dl_params": "null"},
            {"ue_ul_handle": "null", "dl_reply": "null", "command_mode": "null", "dl_params": "null"},
            {"ue_ul_handle": args.second_function, "dl_reply": "gmm_status", "command_mode": "send", "dl_params": param_dict}
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
            {"ue_ul_handle": args.second_function, "dl_reply": "gmm_status", "command_mode": "send", "dl_params": param_dict},
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
        "gmm_cause": gmm_cause_values,
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
