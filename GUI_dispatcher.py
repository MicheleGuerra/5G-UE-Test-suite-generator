import tkinter as tk
from tkinter import ttk
import subprocess

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

    update_second_function_default()


def update_second_function_default():
    first_function = function_var.get()
    default_values = {
        "generate_registration_reject_tests": "registration_request",
        "generate_identity_request_tests": "identity_response",
        "generate_authentication_request_tests": "identity_response",
        "generate_security_mode_command_tests": "authentication_response",
    }
    default_value = default_values.get(first_function, "default_value_generale")
    second_function_var.set(default_value)


def call_test_script():
    script_name = function_var.get()

    second_function = second_function_var.get()
    
    dl_params = []
    num_tests = int(num_tests_var.get())
    
    for dl_param, var in dl_param_vars.items():
        if var.get():
            dl_params.append(dl_param)
    
    cmd = ["python", f"test_case_generators/{script_name}.py"]
    if dl_params:
        cmd += ['--dl_params'] + dl_params
    if num_tests:
        cmd.append(f'--num_tests={num_tests}')
    
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
ttk.Label(frame, text="Select Downlink:").grid(row=0, column=0, sticky=tk.W)
function_var = tk.StringVar()
function_combo = ttk.Combobox(frame, textvariable=function_var, width=35)
function_combo.grid(row=0, column=1, sticky=tk.W)
function_combo['values'] = ("generate_registration_reject_tests", "generate_identity_request_tests", "generate_authentication_request_tests", "generate_security_mode_command_tests")
function_var.trace("w", update_dl_params)

# Initialize second function combo box
ttk.Label(frame, text="Select Uplink:").grid(row=1, column=0, sticky=tk.W)
second_function_var = tk.StringVar()
second_function_combo = ttk.Combobox(frame, textvariable=second_function_var, width=35)
second_function_combo.grid(row=1, column=1, sticky=tk.W)
second_function_combo['values'] = ("registration_request", "identity_response", "authentication_response")

# Initialize DL params checkbuttons
dl_params_frame = ttk.Frame(frame)
dl_params_frame.grid(row=2, columnspan=2, sticky=(tk.W, tk.E))

dl_params_per_function = {
    "generate_registration_reject_tests": ["gmm_cause", "security_header_type", "t3346_value", "t3502_value", "nssai", "eap"],
    "generate_identity_request_tests": ["identity_type", "security_header_type"],
    "generate_authentication_request_tests": ["ngksi_tsc", "ngksi_ksi", "abba", "authentication_parameter_rand", "authentication_parameter_autn", "eap_message", "security_header_type"],
    "generate_security_mode_command_tests": ["nas_security_encryption", "nas_security_integrity", "security_header_type", "selected_eps_nas_security_algorithms", "eap_message", "imeisv_request", "ngksi_tsc", "ngksi_ksi", "abba", "replayed_ue_security_capabilities_nr_ea", "replayed_ue_security_capabilities_nr_ia", "replayed_ue_security_capabilities_eutra_ea", "replayed_ue_security_capabilities_eutra_ia", "replayed_ue_security_capabilities_gea", "additional_security_information_retransmission", "additional_security_information_derivation", "replayed_s1_ue_security_capabilities_nr_ea", "replayed_s1_ue_security_capabilities_nr_ia", "replayed_s1_ue_security_capabilities_eutra_ea", "replayed_s1_ue_security_capabilities_eutra_ia"]
}

dl_param_vars = {}

# Initialize seed entry
ttk.Label(frame, text="Seed:").grid(row=3, column=0, sticky=tk.W)
seed_var = tk.StringVar()
seed_entry = ttk.Entry(frame, textvariable=seed_var, width=10)
seed_entry.grid(row=3, column=1, sticky=tk.W)

# Initialize num_tests entry
ttk.Label(frame, text="Number of Tests:").grid(row=4, column=0, sticky=tk.W)
num_tests_var = tk.StringVar()
num_tests_entry = ttk.Entry(frame, textvariable=num_tests_var, width=10)
num_tests_entry.grid(row=4, column=1, sticky=tk.W)

# Initialize execute button
ttk.Button(frame, text="Execute", command=call_test_script).grid(row=5, columnspan=2)

root.mainloop()
