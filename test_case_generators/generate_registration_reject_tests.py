# Parametrizzato su funzione 1
import os
import argparse
import json
import random

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

timer_values = ["100"]
nssai_values = ["01234567890123456789012345678901234567890123456789012345678901234567890123456789"]
eap_values = ["100"]

def generate_test_case(params_to_include, test_id):
    param_values = {
        "gmm_cause": gmm_cause_values,
        "security_header_type": security_header_type_values,
        "t3502_value": timer_values,
        "t3466_value": timer_values,
        "nssai": nssai_values,
        "eap": eap_values
    }

    param_dict = {}

    # Create directory if not exists
    directory_name = "generate_registration_reject_tests"
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)


    for param in params_to_include:
        if param in param_values:
            param_dict[param] = random.choice(param_values[param])



     # Controlli aggiuntivi per combinazioni specifiche
    gmm_cause = param_dict.get("gmm_cause", None)

    # Regola 1: Se la causa è "CONGESTION", allora t3502_value o t3466_value dovrebbe essere impostato su 10000
    if gmm_cause == "OGS_5GMM_CAUSE_CONGESTION":
        special_param = random.choice(["t3502_value", "t3466_value"])
        param_dict[special_param] = "10000"

    # Regola 2: Per cause illegali, utilizzare solo header di sicurezza "PLAIN_NAS_MESSAGE"
    if gmm_cause in ["OGS_5GMM_CAUSE_ILLEGAL_UE", "OGS_5GMM_CAUSE_ILLEGAL_ME"]:
        if "security_header_type" in param_dict:
            param_dict["security_header_type"] = "OGS_NAS_SECURITY_HEADER_PLAIN_NAS_MESSAGE"

    # Regola 3: Se la causa è una di quelle che indicano un'area non consentita, allora nssai dovrebbe essere rimosso
    if gmm_cause in ["OGS_5GMM_CAUSE_PLMN_NOT_ALLOWED", "OGS_5GMM_CAUSE_TRACKING_AREA_NOT_ALLOWED"]:
        if "nssai" in param_dict:
            del param_dict["nssai"]

    # Regola 4: Per "N1_MODE_NOT_ALLOWED", dovrebbe essere presente t3346_value
    if gmm_cause == "OGS_5GMM_CAUSE_N1_MODE_NOT_ALLOWED":
        param_dict["t3346_value"] = random.choice(timer_values)

    # Regola 5: Per "NON_3GPP_ACCESS_TO_5GCN_NOT_ALLOWED", l'EAP Message dovrebbe essere vuoto
    if gmm_cause == "OGS_5GMM_CAUSE_NON_3GPP_ACCESS_TO_5GCN_NOT_ALLOWED":
        param_dict["eap"] = ""

    # Regola 6: Per "UE_SECURITY_CAPABILITIES_MISMATCH", l'header di sicurezza dovrebbe essere impostato su "INTEGRITY_PROTECTED"
    if gmm_cause == "OGS_5GMM_CAUSE_UE_SECURITY_CAPABILITIES_MISMATCH":
        param_dict["security_header_type"] = "OGS_NAS_SECURITY_HEADER_INTEGRITY_PROTECTED"



    # Handle special cases
    # if "gmm_cause" in params_to_include and param_dict.get("gmm_cause") == "OGS_5GMM_CAUSE_CONGESTION":
    #     special_param = random.choice(["t3502_value", "t3466_value"])
    #     param_dict[special_param] = 10000

    # Add the special cases for timers
    #if "t3346_value" in param_dict:
     #   param_dict["gmm_cause"] = "OGS_5GMM_CAUSE_N1_MODE_NOT_ALLOWED"

    #if "t3502_value" in param_dict:
    #    param_dict["gmm_cause"] = "OGS_5GMM_CAUSE_N1_MODE_NOT_ALLOWED"

    # Add the special case for security_header_type
    # if "security_header_type" in param_dict:
    #     param_dict["gmm_cause"] = "OGS_5GMM_CAUSE_N1_MODE_NOT_ALLOWED"

    # Add the special case for nssai
    #if "rejected_nssai" in param_dict:
    #    param_dict["gmm_cause"] = "OGS_5GMM_CAUSE_N1_MODE_NOT_ALLOWED"

    # Add the special case for eap
    #if "eap_message" in param_dict:
    #    param_dict["gmm_cause"] = "OGS_5GMM_CAUSE_N1_MODE_NOT_ALLOWED"


    output_data = [
        {"ue_ul_handle": "null", "dl_reply": "null", "command_mode": "null", "dl_params": "null"},
        {"ue_ul_handle": args.second_function, "dl_reply": "registration_reject", "command_mode": "send", "dl_params": param_dict},
        {"ue_ul_handle": "null", "dl_reply": "null", "command_mode": "null", "dl_params": "null"}
    ]

    output_filename = f'{directory_name}/test_case_{test_id}.json'
    with open(output_filename, 'w') as json_file:
        json.dump(output_data, json_file, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Test Cases")
    parser.add_argument("--dl_params", nargs='+', help="List of dl_params to include in test cases", default=[])
    parser.add_argument("--num_tests", type=int, help="Number of test cases to generate", default=1)
    parser.add_argument('--second_function', type=str, help='Nome della seconda funzione selezionata.')
    parser.add_argument('--seed', type=int, help='The random seed')
    args = parser.parse_args()

    print(f"Received dl_params: {args.dl_params}")
    print(f"Received num_tests: {args.num_tests}")

    if args.seed is not None:
        random.seed(args.seed)


    for test_id in range(args.num_tests):
        generate_test_case(args.dl_params, test_id)