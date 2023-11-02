import os
import argparse
import json
import random
from itertools import product, chain, combinations

# Definisci tutti i possibili valori per ogni parametro
gmm_cause_values = [
    "OGS_5GMM_CAUSE_ILLEGAL_UE",
    "OGS_5GMM_CAUSE_ILLEGAL_ME",
    "OGS_5GMM_CAUSE_UE_IDENTITY_CANNOT_BE_DERIVED_BY_THE_NETWORK",
    "OGS_5GMM_CAUSE_IMPLICITLY_DE_REGISTERED",
    "OGS_5GMM_CAUSE_IMPLICITLY_UNAUTHORIZED_UPLINK_DATA_DIRECT_COMMUNICATION",
    "OGS_5GMM_CAUSE_IMPLICITLY_UNAUTHORIZED_UPLINK_DATA_STATUS_REPORT_ONLY",
    "OGS_5GMM_CAUSE_IMEI_NOT_ACCEPTED",
    "OGS_5GMM_CAUSE_EPS_SERVICES_NOT_ALLOWED",
    "OGS_5GMM_CAUSE_EPS_SERVICES_AND_NON_EPS_SERVICES_NOT_ALLOWED",
    "OGS_5GMM_CAUSE_PLMN_NOT_ALLOWED",
    "OGS_5GMM_CAUSE_TA_NOT_ALLOWED",
    "OGS_5GMM_CAUSE_ROAMING_NOT_ALLOWED_IN_TA",
    "OGS_5GMM_CAUSE_NO_SUITABLE_CELLS_IN_TA",
    "OGS_5GMM_CAUSE_MAC_FAILURE",
    "OGS_5GMM_CAUSE_SYNCH_FAILURE",
    "OGS_5GMM_CAUSE_CONGESTION",
    "OGS_5GMM_CAUSE_UE_SECURITY_MISMATCH",
    "OGS_5GMM_CAUSE_SECURITY_MODE_REJECTED_UNSPECIFIED",
    "OGS_5GMM_CAUSE_NON_5G_SA_SIGNALLING_SERVICES_NOT_ALLOWED",
    "OGS_5GMM_CAUSE_CS_DOMAIN_NOT_AVAILABLE",
    "OGS_5GMM_CAUSE_ESM_FAILURE",
    "OGS_5GMM_CAUSE_MAC_FAILURE_CS_FALLBACK_NOT_PREFERRED",
    "OGS_5GMM_CAUSE_LADN_NOT_AVAILABLE",
    "OGS_5GMM_CAUSE_MAXIMUM_NUMBER_OF_PDU_SESSIONS_REACHED",
    "OGS_5GMM_CAUSE_INSUFFICIENT_RESOURCES_FOR_SLICE_AND_DNN",
    "OGS_5GMM_CAUSE_NOT_SUPPORTED_SSC_MODE",
    "OGS_5GMM_CAUSE_INSUFFICIENT_RESOURCES_FOR_SPECIFIC_SLICE_AND_DNN",
    "OGS_5GMM_CAUSE_MISSING_OR_UNKNOWN_DNN",
    "OGS_5GMM_CAUSE_MISSING_OR_UNKNOWN_SLICE_TYPE",
    "OGS_5GMM_CAUSE_INVALID_PTI_VALUE",
    "OGS_5GMM_CAUSE_MAXIMUM_DATA_RATE_PER_UE_FOR_USER_PLANE_INTEGRITY_PROTECTION_IS_TOO_LOW",
    "OGS_5GMM_CAUSE_SEMANTICALLY_INCORRECT_MESSAGE",
    "OGS_5GMM_CAUSE_INVALID_MANDATORY_INFORMATION",
    "OGS_5GMM_CAUSE_MESSAGE_TYPE_NON_EXISTENT_OR_NOT_IMPLEMENTED",
    "OGS_5GMM_CAUSE_MESSAGE_TYPE_NOT_COMPATIBLE_WITH_THE_PROTOCOL_STATE",
    "OGS_5GMM_CAUSE_INFORMATION_ELEMENT_NON_EXISTENT_OR_NOT_IMPLEMENTED",
    "OGS_5GMM_CAUSE_CONDITIONAL_IE_ERROR",
    "OGS_5GMM_CAUSE_MESSAGE_NOT_COMPATIBLE_WITH_THE_PROTOCOL_STATE",
    "OGS_5GMM_CAUSE_PROTOCOL_ERROR_UNSPECIFIED",
]

security_header_type_values = [
    "OGS_NAS_SECURITY_HEADER_PLAIN_NAS_MESSAGE",
    "OGS_NAS_SECURITY_HEADER_INTEGRITY_PROTECTED",
    "OGS_NAS_SECURITY_HEADER_INTEGRITY_PROTECTED_AND_CIPHERED",
    "OGS_NAS_SECURITY_HEADER_INTEGRITY_PROTECTED_AND_NEW_SECURITY_CONTEXT",
    "OGS_NAS_SECURITY_HEADER_INTEGRITY_PROTECTED_AND_CIPHERED_WITH_NEW_SECURITY_CONTEXT",
]

t3346_values = ["100"]  # Lista di valori per t3346_value
t3448_values = ["100"]  # Lista di valori per t3448_value
eap_values = ["100"]  # Lista di valori per eap_message
pdu_session_status_values = ["100"]  # Lista di valori per pdu_session_status

def generate_test_case(params_to_include, test_id):
    param_values = {
        "gmm_cause": gmm_cause_values,
        "security_header_type": security_header_type_values,
        "t3346_value": t3346_values,
        "t3448_value": t3448_values,
        "eap_message": eap_values,
        "pdu_session_status": pdu_session_status_values,
    }

    param_dict = {}
    
    directory_name = "generate_service_reject_tests"
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    for param in params_to_include:
        if param in param_values:
            param_dict[param] = random.choice(param_values[param])
    
    # Aggiungi qui eventuali regole o logiche speciali per generare casi di test
    
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
            {"ue_ul_handle": args.second_function, "dl_reply": "service_reject", "command_mode": "send", "dl_params": param_dict}
        ]
    else:
        output_data = [
            {"ue_ul_handle": "null", "dl_reply": "null", "command_mode": "null", "dl_params": "null"},
            {"ue_ul_handle": args.second_function, "dl_reply": "service_reject", "command_mode": "send", "dl_params": param_dict},
            {"ue_ul_handle": "null", "dl_reply": "null", "command_mode": "null", "dl_params": "null"}
        ]

    output_filename = f'{directory_name}/test_case_{test_id}.json'
    with open(output_filename, 'w') as json_file:
        json.dump(output_data, json_file, indent=2)

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1))

def generate_all_possible_test_cases(params_to_include):
    param_values = {
        "gmm_cause": gmm_cause_values,
        "security_header_type": security_header_type_values,
        "t3346_value": t3346_values,
        "t3448_value": t3448_values,
        "eap_message": eap_values,
        "pdu_session_status": pdu_session_status_values,
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
            print(f"Generating {test_id + 1} test cases")
            generate_test_case(selected_params, test_id)
