while True:
    num1 = int(input("enter first number: "))   
    num2 = int(input("enter second number: "))
    operator = input("enter operation u want to perform (-,+,/,*,%,^): ")


    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    elif operator == "/":
        result = num1 / num2
    elif operator == "*":
        result = num1 * num2
    elif operator == "%":
        result = num1 % num2
    elif operator == "^":
        result = num1 ^ num2
    else:
        print("invalid operator")
        
    print(f"the answer of {num1} and {num2} is = {result}")

    again = input("do u want to calculate again (yes or no): ")
    if again == "no":
        break

