def bruteforce_password():
    # Open the wordlist file
    with open('wordlist.txt', 'r') as wordlist_file:
        wordlist = wordlist_file.read().splitlines()

    # Initialize the search range
    low = 0
    high = len(wordlist) - 1

    # Loop until the search range is valid
    while low <= high:
        mid = (low + high) // 2  # Calculate the mid index
        password = wordlist[mid]  # Get the password at the mid index

        # Print the password and ask for input from the bruteforcer program
        print(password)
        response = input()

        # Check if the response matches the expected output
        if response == 'Correct':
            print(f"The correct password is: {password}")
            return
        elif response == 'Smaller':
            high = mid - 1  # Adjust the high index
        elif response == 'Larger':
            low = mid + 1  # Adjust the low index

    print("Password not found in the wordlist.")


bruteforce_password()
