import tkinter as tk
from tkinter import ttk
import subprocess


# Dizionario dei parametri che possono avere l'opzione "disabled" per specifiche funzioni
params_disabled_for_function = {
    "generate_registration_reject_tests": ["gmm_cause", "security_header_type"],
    "generate_identity_request_tests": ["security_header_type"]
    # Aggiungi altre funzioni e i loro parametri come necessario
}

functions_with_special_checkbox = ["generate_security_mode_command_tests", "generate_registration_accept_tests", "generate_configuration_update_command_tests", "generate_send_service_accept_tests", "generate_send_gmm_status_tests", "generate_send_de_registration_request_tests", "generate_deregistration_accept_tests", "generate_authentication_result_tests"]

def update_dl_params(*args):
    function = function_var.get()
    update_second_function_default()  # Aggiunge questa riga per aggiornare la seconda funzione
    for widget in dl_params_frame.winfo_children():
        widget.destroy()
    
    for i, dl_param in enumerate(dl_params_per_function.get(function, [])):
        var = tk.BooleanVar()
        var.set(True)
        dl_param_vars[dl_param] = var
        ttk.Checkbutton(dl_params_frame, text=dl_param, variable=var).grid(row=i, column=0, sticky=tk.W)

        if dl_param in params_disabled_for_function.get(function, []):
            status_var = tk.StringVar()
            status_var.set("enabled")
            dl_param_status[dl_param] = status_var
            ttk.Combobox(dl_params_frame, textvariable=status_var, values=("enabled", "disabled"), width=10).grid(row=i, column=1, sticky=tk.W)

    update_second_function_default()

    # Update visibility of the SEND PLAIN MESSAGE checkbox
    if function in functions_with_special_checkbox:
        special_checkbox.grid()
    else:
        special_checkbox.grid_remove()


def update_second_function_default():
    first_function = function_var.get()
    default_values = {
        "generate_registration_reject_tests": "registration_request",
        "generate_identity_request_tests": "identity_response",
        "generate_authentication_request_tests": "identity_response",
        "generate_security_mode_command_tests": "authentication_response",
        "generate_send_service_reject_tests": "authentication_response",
        "generate_send_de_registration_request_tests": "authentication_response",
        "generate_send_gmm_status_tests": "authentication_response",
        "generate_send_service_accept_tests": "service_request",
        "generate_configuration_update_command_tests": "authentication_response",
        "generate_registration_accept_tests": "registration_request",
        "generate_authentication_result_tests": "authentication_response",
        "generate_authentication_reject_tests": "authentication_response",
        "generate_deregistration_accept_tests": "service_request"
    }
    default_value = default_values.get(first_function, "default_value_generale")
    second_function_var.set(default_value)


def call_test_script():
    script_name = function_var.get()

    second_function = second_function_var.get()
    
    dl_params = []
    disabled_params = []
    num_tests = int(num_tests_var.get())
    
    for dl_param, var in dl_param_vars.items():
        if var.get():
            if dl_param in dl_param_status and dl_param_status[dl_param].get() == "disabled":
                disabled_params.append(dl_param)
                dl_params.append(dl_param)
            else:
                dl_params.append(dl_param)
    
    cmd = ["python", f"test_case_generators/{script_name}.py"]
    if dl_params:
        cmd += ['--dl_params'] + dl_params
    if disabled_params:
        cmd += ['--disabled_params'] + disabled_params
    if num_tests:
        cmd.append(f'--num_tests={num_tests}')
    if special_checkbox_var.get():
        cmd.append(f'--enable_special_option')
    
    cmd.append(f'--second_function={second_function}')

    seed = seed_var.get()
    if seed:
        cmd.append(f'--seed={seed}')
    

    
    subprocess.run(' '.join(cmd), shell=True)

# Initialize main window
root = tk.Tk()
root.title("Dispatcher GUI")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Initialize function combo box
ttk.Label(frame, text="Select Downlink:").grid(row=1, column=0, sticky=tk.W)
function_var = tk.StringVar()
function_combo = ttk.Combobox(frame, textvariable=function_var, width=35)
function_combo.grid(row=1, column=1, sticky=tk.W)
function_combo['values'] = ("generate_registration_reject_tests", "generate_identity_request_tests", "generate_authentication_request_tests", "generate_security_mode_command_tests", "generate_send_service_reject_tests", "generate_send_de_registration_request_tests", "generate_send_gmm_status_tests", "generate_send_service_accept_tests", "generate_configuration_update_command_tests", "generate_registration_accept_tests", "generate_authentication_result_tests", "generate_authentication_reject_tests", "generate_deregistration_accept_tests")
function_var.trace("w", update_dl_params)

# Initialize second function combo box
ttk.Label(frame, text="Select Uplink:").grid(row=0, column=0, sticky=tk.W)
second_function_var = tk.StringVar()
second_function_combo = ttk.Combobox(frame, textvariable=second_function_var, width=35)
second_function_combo.grid(row=0, column=1, sticky=tk.W)
second_function_combo['values'] = ("registration_request", "identity_response", "authentication_response", "service_request", "security_mode_complete", "registration_complete", "ul_nas_transport", "gmm_status", "configuration_update_complete", "deregistration_request", "deregistration_accept")

# Initialize DL params checkbuttons
dl_params_frame = ttk.Frame(frame)
dl_params_frame.grid(row=2, columnspan=2, sticky=(tk.W, tk.E))

dl_params_per_function = {
    "generate_registration_reject_tests": ["gmm_cause", "security_header_type", "t3346_value", "t3502_value", "nssai", "eap"],
    "generate_identity_request_tests": ["identity_type", "security_header_type"],
    "generate_authentication_request_tests": ["ngksi_tsc", "ngksi_ksi", "abba", "authentication_parameter_rand", "authentication_parameter_autn", "eap_message", "security_header_type"],
    "generate_security_mode_command_tests": ["nas_security_encryption", "nas_security_integrity", "security_header_type", "selected_eps_nas_security_algorithms", "eap_message", "imeisv_request", "ngksi_tsc", "ngksi_ksi", "abba", "replayed_ue_security_capabilities_nr_ea", "replayed_ue_security_capabilities_nr_ia", "replayed_ue_security_capabilities_eutra_ea", "replayed_ue_security_capabilities_eutra_ia", "replayed_ue_security_capabilities_gea", "additional_security_information_retransmission", "additional_security_information_derivation", "replayed_s1_ue_security_capabilities_nr_ea", "replayed_s1_ue_security_capabilities_nr_ia", "replayed_s1_ue_security_capabilities_eutra_ea", "replayed_s1_ue_security_capabilities_eutra_ia"],
    "generate_send_service_reject_tests": ["gmm_cause", "security_header_type", "t3346_value", "t3448_value", "pdu_session_status", "eap_message"],
    "generate_send_de_registration_request_tests": ["gmm_cause", "security_header_type", "t3346_value", "de_registration_type.switch_off", "de_registration_type.tsc", "de_registration_type.ksi", "de_registration_type.re_registration_required", "de_registration_type.access_type", "rejected_nssai"],
    "generate_send_gmm_status_tests": ["gmm_cause", "security_header_type"],
    "generate_send_service_accept_tests": ["security_header_type", "pdu_session_status_psi", "pdu_session_reactivation_result_psi", "pdu_session_reactivation_result_error_cause", "t3448_value", "eap_message"],
    "generate_configuration_update_command_tests": ["network_daylight_saving_time", "sms_indication_type", "security_header_type"],
    "generate_registration_accept_tests": ["security_header_type", "registration_result_value", "equivalent_plmns_mcc", "network_feature_support_ims", "pdu_session_status_psi", "pdu_session_reactivation_result_psi", "nssai", "eap"],
    "generate_authentication_result_tests": ["security_header_type", "ngksi_tsc", "ngksi_ksi", "eap"],
    "generate_authentication_reject_tests": ["security_header_type"],
    "generate_deregistration_accept_tests": ["security_header_type"]
}

dl_param_vars = {}
dl_param_status = {}
special_checkbox_var = tk.BooleanVar(value=False)

# Initialize plain message checkbox
special_checkbox = ttk.Checkbutton(frame, text="Send as plain message", variable=special_checkbox_var)
special_checkbox.grid(row=3, column=0, sticky=tk.W)

# Initialize seed entry
ttk.Label(frame, text="Seed:").grid(row=4, column=0, sticky=tk.W)
seed_var = tk.StringVar()
seed_entry = ttk.Entry(frame, textvariable=seed_var, width=10)
seed_entry.grid(row=4, column=1, sticky=tk.W)

# Initialize num_tests entry
ttk.Label(frame, text="Number of Tests:").grid(row=5, column=0, sticky=tk.W)
num_tests_var = tk.StringVar()
num_tests_entry = ttk.Entry(frame, textvariable=num_tests_var, width=10)
num_tests_entry.grid(row=5, column=1, sticky=tk.W)

# Initialize execute button
ttk.Button(frame, text="Execute", command=call_test_script).grid(row=6, columnspan=2)

root.mainloop()
