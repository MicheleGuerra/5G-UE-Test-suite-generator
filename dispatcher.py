#dispatcher

import argparse
import subprocess

def call_test_script(script_name, dl_params, num_tests):
    cmd = ["python", f"{script_name}.py"]
    if dl_params:
        dl_params_str = ','.join(dl_params)
        cmd += ['--dl_params'] + dl_params
    if num_tests:
        cmd.append(f'--num_tests={num_tests}')
    
    subprocess.run(' '.join(cmd), shell=True)

def main():
    parser = argparse.ArgumentParser(description="Generate test cases based on the given function.")
    parser.add_argument("--function", type=str, required=True, help="Name of the C function for which to generate test cases.")
    parser.add_argument("--dl_params", type=str, nargs="+", help="List of dl_params to include in the test cases.")
    parser.add_argument("--num_tests", type=int, help="Number of test cases to generate.")

    args = parser.parse_args()

    if args.function == "user_nas_5gs_send_registration_reject":
        call_test_script("generate_registration_reject_tests", args.dl_params, args.num_tests)
    elif args.function == "user_nas_5gs_send_service_reject":
        call_test_script("generate_service_reject_tests", args.dl_params, args.num_tests)
    # Add more elif blocks here for other C functions
    else:
        print(f"Unknown function: {args.function}")

if __name__ == "__main__":
    main()
