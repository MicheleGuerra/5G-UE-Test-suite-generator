# Parametrizzato su funzione 1
from ast import arg
import os
import argparse
import json
import random
from itertools import product
from itertools import chain, combinations

# Define all possible values for each parameter
nas_security_encryption_values =[
	"OGS_NAS_SECURITY_ALGORITHMS_NEA0",
	"OGS_NAS_SECURITY_ALGORITHMS_128_NEA1",
	"OGS_NAS_SECURITY_ALGORITHMS_128_NEA2",
	"OGS_NAS_SECURITY_ALGORITHMS_128_NEA3",
	"OGS_NAS_SECURITY_ALGORITHMS_NEA4",
	"OGS_NAS_SECURITY_ALGORITHMS_NEA5",
	"OGS_NAS_SECURITY_ALGORITHMS_NEA6",
	"OGS_NAS_SECURITY_ALGORITHMS_NEA7",
	"OGS_NAS_SECURITY_ALGORITHMS_EEA0",
	"OGS_NAS_SECURITY_ALGORITHMS_128_EEA1",
	"OGS_NAS_SECURITY_ALGORITHMS_128_EEA2",
	"OGS_NAS_SECURITY_ALGORITHMS_128_EEA3"
    ]


nas_security_integrity_values =[
	"OGS_NAS_SECURITY_ALGORITHMS_NIA0",
	"OGS_NAS_SECURITY_ALGORITHMS_128_NIA1",
	"OGS_NAS_SECURITY_ALGORITHMS_128_NIA2",
	"OGS_NAS_SECURITY_ALGORITHMS_128_NIA3",
	"OGS_NAS_SECURITY_ALGORITHMS_NIA4",
	"OGS_NAS_SECURITY_ALGORITHMS_NIA5",
	"OGS_NAS_SECURITY_ALGORITHMS_NIA6",
	"OGS_NAS_SECURITY_ALGORITHMS_NIA7",
	"OGS_NAS_SECURITY_ALGORITHMS_EIA0",
	"OGS_NAS_SECURITY_ALGORITHMS_128_EIA1",
	"OGS_NAS_SECURITY_ALGORITHMS_128_EIA2",
	"OGS_NAS_SECURITY_ALGORITHMS_128_EIA3"
    ]



security_header_type_values =[
	"OGS_NAS_SECURITY_HEADER_PLAIN_NAS_MESSAGE",
	"OGS_NAS_SECURITY_HEADER_INTEGRITY_PROTECTED",
	"OGS_NAS_SECURITY_HEADER_INTEGRITY_PROTECTED_AND_NEW_SECURITY_CONTEXT",
	"OGS_NAS_SECURITY_HEADER_INTEGRITY_PROTECTED_AND_PARTICALLY_CIPHTERD",
	"OGS_NAS_SECURITY_HEADER_FOR_SERVICE_REQUEST_MESSAGE",
	"OGS_NAS_SECURITY_HEADER_INTEGRITY_PROTECTED_AND_CIPHTERD_WITH_NEW_INTEGRITY_CONTEXT",
	"OGS_NAS_SECURITY_HEADER_INTEGRITY_PROTECTED_AND_CIPHERED"
    ]


selected_eps_nas_security_algorithms_values =[
	"OGS_NAS_SECURITY_ALGORITHMS_NEA0",
	"OGS_NAS_SECURITY_ALGORITHMS_128_NEA1",
	"OGS_NAS_SECURITY_ALGORITHMS_128_NEA2",
	"OGS_NAS_SECURITY_ALGORITHMS_128_NEA3",
	"OGS_NAS_SECURITY_ALGORITHMS_NEA4",
	"OGS_NAS_SECURITY_ALGORITHMS_NEA5",
	"OGS_NAS_SECURITY_ALGORITHMS_NEA6",
	"OGS_NAS_SECURITY_ALGORITHMS_NEA7",
	"OGS_NAS_SECURITY_ALGORITHMS_EEA0",
	"OGS_NAS_SECURITY_ALGORITHMS_128_EEA1",
	"OGS_NAS_SECURITY_ALGORITHMS_128_EEA2",
	"OGS_NAS_SECURITY_ALGORITHMS_128_EEA3",	
	"OGS_NAS_SECURITY_ALGORITHMS_NIA0",
	"OGS_NAS_SECURITY_ALGORITHMS_128_NIA1",
	"OGS_NAS_SECURITY_ALGORITHMS_128_NIA2",
	"OGS_NAS_SECURITY_ALGORITHMS_128_NIA3",
	"OGS_NAS_SECURITY_ALGORITHMS_NIA4",
	"OGS_NAS_SECURITY_ALGORITHMS_NIA5",
	"OGS_NAS_SECURITY_ALGORITHMS_NIA6",
	"OGS_NAS_SECURITY_ALGORITHMS_NIA7",
	"OGS_NAS_SECURITY_ALGORITHMS_EIA0",
	"OGS_NAS_SECURITY_ALGORITHMS_128_EIA1",
	"OGS_NAS_SECURITY_ALGORITHMS_128_EIA2",
	"OGS_NAS_SECURITY_ALGORITHMS_128_EIA3"	
    ]


eap_values =[
	"100"
    ]


imeisv_request_values =[
	"OGS_NAS_IMEISV_NOT_REQUESTED"	
    ]
	

ngksi_tsc_values =[
	"1"
    ]

ngksi_ksi_values =[
	"1"
    ]


abba_values =[
	"1"
    ]


replayed_ue_security_capabilities_nr_ea_values =[
	"1"
    ]

replayed_ue_security_capabilities_nr_ia_values =[
	"1"
    ]

replayed_ue_security_capabilities_eutra_ea_values =[
	"1"
    ]

replayed_ue_security_capabilities_eutra_ia_values =[
	"1"
    ]



replayed_ue_security_capabilities_gea_values =[
	"1"
    ]


additional_security_information_retransmission_values =[
	"1"
    ]
    
    
additional_security_information_derivation_values =[
	"1"
    ]
    
replayed_s1_ue_security_capabilities_nr_ea_values =[
	"1"
    ]
    
replayed_s1_ue_security_capabilities_nr_ia_values =[
	"1"
    ]
    
replayed_s1_ue_security_capabilities_eutra_ea_values =[
	"1"
    ]
    

replayed_s1_ue_security_capabilities_eutra_ia_values =[
	"1"
    ]

def generate_test_case(params_to_include, test_id):
    param_values = {
        'nas_security_encryption': nas_security_encryption_values,
        'nas_security_integrity': nas_security_integrity_values,
        'security_header_type': security_header_type_values,
        'selected_eps_nas_security_algorithms': selected_eps_nas_security_algorithms_values,
        'eap_message': eap_values,
        'imeisv_request': imeisv_request_values,
        'ngksi_tsc': ngksi_tsc_values,
        'ngksi_ksi': ngksi_ksi_values,
        'abba': abba_values,
        'replayed_ue_security_capabilities_nr_ea': replayed_ue_security_capabilities_nr_ea_values,
        'replayed_ue_security_capabilities_nr_ia': replayed_ue_security_capabilities_nr_ia_values,
        'replayed_ue_security_capabilities_eutra_ea': replayed_ue_security_capabilities_eutra_ea_values,
        'replayed_ue_security_capabilities_eutra_ia': replayed_ue_security_capabilities_eutra_ia_values,
        'replayed_ue_security_capabilities_gea': replayed_ue_security_capabilities_gea_values,
        'additional_security_information_retransmission': additional_security_information_retransmission_values,
        'additional_security_information_derivation': additional_security_information_derivation_values,
        'replayed_s1_ue_security_capabilities_nr_ea': replayed_s1_ue_security_capabilities_nr_ea_values,
        'replayed_s1_ue_security_capabilities_nr_ia': replayed_s1_ue_security_capabilities_nr_ia_values,
        'replayed_s1_ue_security_capabilities_eutra_ea': replayed_s1_ue_security_capabilities_eutra_ea_values,
        'replayed_s1_ue_security_capabilities_eutra_ia': replayed_s1_ue_security_capabilities_eutra_ia_values
    }

    param_dict = {}


    # Create directory if not exists
    directory_name = "generate_security_mode_command_tests"
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
        param_dict["security_mode_command_security"] = "disabled"

    if args.second_function in functions_for_third_row:
        output_data = [
            {"ue_ul_handle": "null", "dl_reply": "null", "command_mode": "null", "dl_params": "null"},
            {"ue_ul_handle": "null", "dl_reply": "null", "command_mode": "null", "dl_params": "null"},
            {"ue_ul_handle": args.second_function, "dl_reply": "security_mode_command", "command_mode": "send", "dl_params": param_dict}
        ]
    else:
        output_data = [
            {"ue_ul_handle": "null", "dl_reply": "null", "command_mode": "null", "dl_params": "null"},
            {"ue_ul_handle": args.second_function, "dl_reply": "security_mode_command", "command_mode": "send", "dl_params": param_dict},
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
        'nas_security_encryption': nas_security_encryption_values,
        'nas_security_integrity': nas_security_integrity_values,
        'security_header_type': security_header_type_values,
        'selected_eps_nas_security_algorithms': selected_eps_nas_security_algorithms_values,
        'eap_message': eap_values,
        'imeisv_request': imeisv_request_values,
        'ngksi_tsc': ngksi_tsc_values,
        'ngksi_ksi': ngksi_ksi_values,
        'abba': abba_values,
        'replayed_ue_security_capabilities_nr_ea': replayed_ue_security_capabilities_nr_ea_values,
        'replayed_ue_security_capabilities_nr_ia': replayed_ue_security_capabilities_nr_ia_values,
        'replayed_ue_security_capabilities_eutra_ea': replayed_ue_security_capabilities_eutra_ea_values,
        'replayed_ue_security_capabilities_eutra_ia': replayed_ue_security_capabilities_eutra_ia_values,
        'replayed_ue_security_capabilities_gea': replayed_ue_security_capabilities_gea_values,
        'additional_security_information_retransmission': additional_security_information_retransmission_values,
        'additional_security_information_derivation': additional_security_information_derivation_values,
        'replayed_s1_ue_security_capabilities_nr_ea': replayed_s1_ue_security_capabilities_nr_ea_values,
        'replayed_s1_ue_security_capabilities_nr_ia': replayed_s1_ue_security_capabilities_nr_ia_values,
        'replayed_s1_ue_security_capabilities_eutra_ea': replayed_s1_ue_security_capabilities_eutra_ea_values,
        'replayed_s1_ue_security_capabilities_eutra_ia': replayed_s1_ue_security_capabilities_eutra_ia_values
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
        print("Using all selected dl_params")
        generate_test_case(args.dl_params, 0)
    elif args.num_tests is None:
        print("Generating all possible test cases")
        generate_all_possible_test_cases(args.dl_params)
    else:
        for test_id in range(args.num_tests):
            selected_params = random.choice(all_param_combinations)
            print(f"Generating test case with params: {selected_params}")
            print(f"Generating {test_id + 1} test cases")
            generate_test_case(selected_params, test_id)