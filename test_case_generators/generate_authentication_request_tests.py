import argparse
import json
import random

# Define all possible values for each parameter
ngksi_tsc_values = ["0"]
ngksi_ksi_values = ["0"]
abba_values = ["0"]
authentication_parameter_rand_values = ["0"]
authentication_parameter_autn_values = ["0"]
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

    output_data = [
        {"ue_ul_handle": "null", "dl_reply": "null", "command_mode": "null", "dl_params": "null"},
        {"ue_ul_handle": args.second_function, "dl_reply": "authentication_request", "command_mode": "send", "dl_params": param_dict},
        {"ue_ul_handle": "null", "dl_reply": "null", "command_mode": "null", "dl_params": "null"}
    ]

    output_filename = f'{directory_name}/test_case_{test_id}.json'
    with open(output_filename, 'w') as json_file:
        json.dump(output_data, json_file, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Test Cases")
    parser.add_argument("--dl_params", nargs='+', help="List of dl_params to include in test cases", default=[])
    parser.add_argument("--num_tests", type=int, help="Number of test cases to generate", default=1)
    parser.add_argument('--second_function', type=str, help='Nome della seconda funzione selezionata.')  # Nuova riga
    args = parser.parse_args()

    print(f"Received dl_params: {args.dl_params}")
    print(f"Received num_tests: {args.num_tests}")

    for test_id in range(args.num_tests):
        generate_test_case(args.dl_params, test_id)