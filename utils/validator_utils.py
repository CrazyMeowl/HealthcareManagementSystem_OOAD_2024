# function to validate if the string contain only digits
# to validate phone_number and ssn
def is_digit_string(input_string,length):
    if length == 0:
        return input_string.isdigit() 
    else:
        return (input_string.isdigit()) and (len(input_string) == length)

