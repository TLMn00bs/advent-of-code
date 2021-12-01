import delegator

class num:
    # We override the basic operators so we can acomplish the precedence rules we have to match
    # Rule 1: "+" and "*" have the same precedence
    # Rule 2: "+" has more precedence than "*"
    def __init__(self, value):
        self.value = value
    
    def __add__(self, number):
        return num(self.value + number.value)

    def __sub__(self, number):
        return num(self.value * number.value)

    def __mul__(self, number):
        return num(self.value + number.value)

# With the sed command, we replace each digit with the "num" constructor, so we can create a "num" object for each digit when we execute "eval()"

def search_1(file):
    command = "sed 's/[0-9]/num(&)/g' {FILE}".format(FILE=file)
    operations = delegator.run(command).out.splitlines()

    result = num(0)

    for operation in operations:
        # The sums and the multiplications must have the same value of precedence, so we simply override the "-" to perform a multiplication
        operation = operation.replace('*', '-')

        result += eval(operation)

    return result.value

def search_2(file):
    command = "sed 's/[0-9]/num(&)/g' {FILE}".format(FILE=file)
    operations = delegator.run(command).out.splitlines()

    result = num(0)

    for operation in operations:
        # The sums must have more precedence than the multiplications, so we simply override the "-" to perform a multiplication and the "*" to perform a sum
        operation = operation.replace('*', '-')
        operation = operation.replace('+', '*')

        result += eval(operation)

    return result.value

file = 'input.txt'
result = search_1(file)
print('Homework 1: {RESULT}'.format(RESULT=result))

result = search_2(file)
print('Homework 2: {RESULT}'.format(RESULT=result))