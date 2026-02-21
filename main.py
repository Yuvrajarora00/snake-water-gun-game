import random

computer = random.choice([-1, 0, 1])
youstr = input("Enter your choice: ")
youdict = {"snake": 1, "water": -1, "gun": 0}
reversedict = {1: "snake", -1: "water", 0: "gun"}

you = youdict[youstr]

print(f"you choose {reversedict[you]}\ncomputer choose {reversedict[computer]}")

if computer == you:
    print("game is draw!")
else:
    
    if computer == -1 and you == 1:
        print("you won!")
    elif computer == -1 and you == 0:
        print("computer won!")
    elif computer == 1 and you == 0:
        print("you won!")
    elif computer == 0 and you == 1:
        print("computer won!")
    elif computer == 0 and you == -1:
        print("you won!")
    elif computer == 1 and you == -1:
        print("computer won")
    else:
        print("something went wrong")
            