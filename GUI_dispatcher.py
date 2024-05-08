import tkinter as tk
from tkinter import ttk
import subprocess
import platform 


# Dizionario dei parametri che possono avere l'opzione "disabled" per specifiche funzioni
params_disabled_for_function = {
}

functions_with_special_checkbox = ["security_mode_command", "registration_accept", "configuration_update_command", "service_accept", "gmm_status", "deregistration_request", "deregistration_accept", "authentication_result"]
all_parametes_functions = ["identity_request", "authentication_request", "security_mode_command", "registration_accept", "configuration_update_command", "service_accept", "service_reject", "gmm_status", "deregistration_accept", "deregistration_request", "authentication_result", "authentication_reject", "registration_reject"]


def update_dl_params(*args):
    function = function_var.get()
    #update_second_function_default()  # Aggiunge questa riga per aggiornare la seconda funzione
    for widget in dl_params_frame.winfo_children():
        widget.destroy()

    ttk.Label(frame, text="Downlink Parameters").grid(row=0, column=0, sticky=tk.W)

    row = 0
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

    #update_second_function_default()
        row += 1

    # Update visibility of the ALL parameters checkbox
    if function in all_parametes_functions:
        use_all_dl_params_checkbox = tk.Checkbutton(dl_params_frame, text="Use all selected params", variable=use_all_dl_params_var)
        use_all_dl_params_checkbox.grid(row=row+1, column=1, sticky=tk.W)
    else:
        use_all_dl_params_checkbox.grid_remove()

    special_checkbox = ttk.Checkbutton(dl_params_frame, text="Send as plain message", variable=special_checkbox_var)
    # Update visibility of the SEND PLAIN MESSAGE checkbox
    ttk.Label(dl_params_frame, text="More Options:").grid(row=row, column=0, sticky=tk.W)
    if function in functions_with_special_checkbox:
        #special_checkbox = ttk.Checkbutton(dl_params_frame, text="Send as plain message", variable=special_checkbox_var)
        special_checkbox.grid(row=row+1, column=0, sticky=tk.W)
    else:
        special_checkbox.grid_remove()

    
    


def update_second_function_default():
    first_function = function_var.get()
    default_values = {
        "registration_reject": "registration_request",
        "identity_request": "identity_response",
        "authentication_request": "identity_response",
        "security_mode_command": "authentication_response",
        "service_reject": "authentication_response",
        "deregistration_request": "authentication_response",
        "gmm_status": "authentication_response",
        "service_accept": "service_request",
        "configuration_update_command": "authentication_response",
        "registration_accept": "registration_request",
        "authentication_result": "authentication_response",
        "authentication_reject": "authentication_response",
        "deregistration_accept": "service_request"
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
    if use_all_dl_params_var.get():
        cmd.append('--use_all_dl_params')
    
    cmd.append(f'--second_function={second_function}')

    seed = seed_var.get()
    if seed:
        cmd.append(f'--seed={seed}')
    

    
    subprocess.run(' '.join(cmd), shell=True)

# Initialize main window
root = tk.Tk()
root.title(" Test Case Generator")

# Set the window icon based on the operating system
if platform.system() == 'Windows':
    root.iconbitmap('5g.ico')  # Imposta l'icona solo se il sistema operativo è Windows

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Initialize function combo box
ttk.Label(frame, text="Select Downlink:").grid(row=1, column=0, sticky=tk.W)
function_var = tk.StringVar()
function_combo = ttk.Combobox(frame, textvariable=function_var, width=35)
function_combo.grid(row=1, column=1, sticky=tk.W)
function_combo['values'] = ("identity_request", "authentication_request", "security_mode_command", "registration_accept", "configuration_update_command", "service_accept", "service_reject", "gmm_status", "deregistration_accept", "deregistration_request", "authentication_result", "authentication_reject", "registration_reject")
function_var.trace("w", update_dl_params)

# Initialize second function combo box
ttk.Label(frame, text="Select Uplink:").grid(row=0, column=0, sticky=tk.W)
second_function_var = tk.StringVar()
second_function_combo = ttk.Combobox(frame, textvariable=second_function_var, width=35)
second_function_combo.grid(row=0, column=1, sticky=tk.W)
second_function_combo['values'] = ("registration_request", "identity_response", "authentication_response", "security_mode_complete", "registration_complete", "ul_nas_transport", "service_request", "gmm_status", "configuration_update_complete", "deregistration_request", "deregistration_accept")

# Initialize DL params checkbuttons
dl_params_frame = ttk.Frame(frame)
dl_params_frame.grid(row=2, columnspan=2, sticky=(tk.W, tk.E))

dl_params_per_function = {
    "registration_reject": ["gmm_cause", "security_header_type", "t3346_value", "t3502_value", "nssai", "eap"],
    "identity_request": ["identity_type", "security_header_type"],
    "authentication_request": ["ngksi_tsc", "ngksi_ksi", "abba", "authentication_parameter_rand", "authentication_parameter_autn", "eap_message", "security_header_type"],
    "security_mode_command": ["nas_security_encryption", "nas_security_integrity", "security_header_type", "selected_eps_nas_security_algorithms", "eap_message", "imeisv_request", "ngksi_tsc", "ngksi_ksi", "abba", "replayed_ue_security_capabilities_nr_ea", "replayed_ue_security_capabilities_nr_ia", "replayed_ue_security_capabilities_eutra_ea", "replayed_ue_security_capabilities_eutra_ia", "replayed_ue_security_capabilities_gea", "additional_security_information_retransmission", "additional_security_information_derivation", "replayed_s1_ue_security_capabilities_nr_ea", "replayed_s1_ue_security_capabilities_nr_ia", "replayed_s1_ue_security_capabilities_eutra_ea", "replayed_s1_ue_security_capabilities_eutra_ia"],
    "service_reject": ["gmm_cause", "security_header_type", "t3346_value", "t3448_value", "pdu_session_status", "eap_message"],
    "deregistration_request": ["gmm_cause", "security_header_type", "t3346_value", "de_registration_type.switch_off", "de_registration_type.tsc", "de_registration_type.ksi", "de_registration_type.re_registration_required", "de_registration_type.access_type", "rejected_nssai"],
    "gmm_status": ["gmm_cause", "security_header_type"],
    "service_accept": ["security_header_type", "pdu_session_status_psi", "pdu_session_reactivation_result_psi", "pdu_session_reactivation_result_error_cause", "t3448_value", "eap_message"],
    "configuration_update_command": ["network_daylight_saving_time", "sms_indication_type", "security_header_type"],
    "registration_accept": ["security_header_type", "registration_result_value", "equivalent_plmns_mcc", "network_feature_support_ims", "pdu_session_status_psi", "pdu_session_reactivation_result_psi", "nssai", "eap"],
    "authentication_result": ["security_header_type", "ngksi_tsc", "ngksi_ksi", "eap"],
    "authentication_reject": ["security_header_type"],
    "deregistration_accept": ["security_header_type"]
}

dl_param_vars = {}
dl_param_status = {}
special_checkbox_var = tk.BooleanVar(value=False)
use_all_dl_params_var = tk.BooleanVar(value=False)

# Initialize plain message checkbox
#special_checkbox = ttk.Checkbutton(frame, text="Send as plain message", variable=special_checkbox_var)
#special_checkbox.grid(row=3, column=0, sticky=tk.W)
#use_all_dl_params_checkbox = tk.Checkbutton(frame, text="Use ALL selected params", variable=use_all_dl_params_var)
#use_all_dl_params_checkbox.grid(row=3, column=0, sticky=tk.W)


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
ttk.Button(frame, text="Execute", command=call_test_script).grid(row=6, columnspan=2, sticky=(tk.W, tk.E), pady=10)

# Initialize the label for the footer text
footer_label = ttk.Label(frame, text="Made with \u2665 by CSP-lab", font=("Helvetica", 10))
footer_label.grid(row=8, columnspan=2, sticky=tk.S, pady=10)



root.mainloop()
