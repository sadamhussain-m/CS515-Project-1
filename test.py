import os
import subprocess

def run_test(program, test_name):
    input_path = f'tests/{program}.{test_name}.in'
    expected_output_path = f'tests/{program}.{test_name}.out'
    expected_arg_output_path = f'tests/{program}.{test_name}.arg.out'
    expected_status_path = f'tests/{program}.{test_name}.status'
    expected_err_path = f'tests/{program}.{test_name}.err'
    timeout_path = f'tests/{program}.{test_name}.timeout'
    zip_path = f'tests/{program}.{test_name}.zip'

    # Read input
    with open(input_path, 'r') as input_file:
        input_data = input_file.read()

    # Set up command
    command = ['python', f'prog/{program}.py']

    # Check if argument output is expected
    if os.path.exists(expected_arg_output_path):
        command.extend(['-l', '-w', '-c'])
        expected_output_path = expected_arg_output_path

    # Check if expected status is provided
    if os.path.exists(expected_status_path):
        with open(expected_status_path, 'r') as status_file:
            expected_status = int(status_file.read())
    else:
        expected_status = 0

    # Check if timeout is specified
    timeout = None
    if os.path.exists(timeout_path):
        with open(timeout_path, 'r') as timeout_file:
            timeout = int(timeout_file.read())

    # Check if setup requires unzipping
    if os.path.exists(zip_path):
        with open(zip_path, 'rb') as zip_file:
            with open(input_path, 'wb') as input_file:
                input_file.write(zip_file.read())

    try:
        # Run the command
        result = subprocess.run(command, input=input_data.encode('utf-8'), capture_output=True, text=True, timeout=timeout)

        # Check if output matches the expected output
        with open(expected_output_path, 'r') as expected_output_file:
            expected_output = expected_output_file.read()
            assert result.stdout == expected_output

        # Check if status matches the expected status
        assert result.returncode == expected_status

        # Check if stderr matches the expected stderr
        if os.path.exists(expected_err_path):
            with open(expected_err_path, 'r') as expected_err_file:
                expected_err = expected_err_file.read()
                assert result.stderr == expected_err

        print(f"OK: {program} {test_name}")

    except subprocess.CalledProcessError as e:
        print(f"FAIL: {program} {test_name} (TestResult.CalledProcessError)")
        print(f"      {e}")

    except subprocess.TimeoutExpired:
        print(f"FAIL: {program} {test_name} (TestResult.TimeoutExpired)")
        print(f"      Test did not complete within the specified timeout")

    except AssertionError:
        print(f"FAIL: {program} {test_name} (TestResult.OutputMismatch)")
        print("      expected:")
        print(f"{expected_output}\n")
        print("      got:")
        print(f"{result.stdout}\n")

if _name_ == '_main_':
    for program in ['gron', 'wc']:
        for test_file in os.listdir('test'):
            if test_file.endswith('.in') and test_file.startswith(f'{program}.'):
                test_name = test_file[len(f'{program}.'):-len('.in')]
                run_test(program, test_name)