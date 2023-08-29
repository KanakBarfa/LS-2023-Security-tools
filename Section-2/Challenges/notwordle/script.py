import subprocess
import string
import itertools

def bruteforce_password():
    password_length = 30
    charset = string.ascii_lowercase + string.digits + '_'
    known_prefix = "pr377y_5u23_7h15_15_n07_w0rd1"  # Replace with the actual known first three characters

    # Generate passwords and check them as they are generated
    for partial_password in itertools.product(charset, repeat=(1)):
        password = known_prefix + ''.join(partial_password)

        # Print the current password being tried
        print(f"Trying password: {password}")

        # Communicate with the bruteforce program
        process = subprocess.Popen(['./notwordle'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        response = process.communicate(input=password.encode())[0].decode().strip()

        # Check the number of correct characters
        num_correct = int(response[83:85])
        if num_correct == password_length:
            print(f"The correct password is: {password}")
            return

    print("Password not found in the brute-force attack.")


bruteforce_password()
