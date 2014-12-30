from getpass import getpass

def get_bool(prompt):
    def valid(user_input):
        if user_input.lower() != 'y' and user_input.lower() != 'n':
            return False
        return True

    user_input = raw_input(prompt)
    while not valid(user_input):
        print "Please enter either 'y' or 'n' (Y/N)."
        user_input = raw_input(prompt)
    return True if user_input.lower() == 'y' else False


def get_string(prompt):
    return raw_input(prompt)


def get_number(prompt, number_type=int):
    def valid(user_input):
        try:
            number_type(user_input)
            return True
        except ValueError:
            return False

    user_input = raw_input(prompt)
    while not valid(user_input):
        print "Please enter a number in the proper format."
        user_input = raw_input(prompt)
    return number_type(user_input)


def get_hidden_string(prompt):
    return getpass(prompt)


def get_password(first_prompt, second_prompt,
                 mismatch_message = "Passwords do not match.  Please try again."):
    while True:
        password = get_hidden_string(first_prompt)
        if password == get_hidden_string(second_prompt):
            return password
        else:
            print mismatch_message
