import sys
import os 
from termcolor import colored

from goodstuff.send import send as s
from goodstuff.recv import recv as r
from goodstuff.d import d
def help():
    print(colored("This is a git alternative ","green"))

    print(colored("These are the commands that u can execute:","magenta"))

    print(colored("1.gilma vechuko ","green"))
    print(colored("2.gilma vangiko ","green"))
    print(colored("3.gilma sethupo ","green"))
    

    
def main():
    if len(sys.argv) != 2 :
        print(colored("you are using it wrong "),"red")
        help()
        sys.exit(1)
    arg = sys.argv[1]

    if arg == "vangiko":
        print(colored("receiving data...","green"))
        r()
        print(colored("Well That Was QUICK","green"))

    elif arg == "vechuko":
        print(colored("sending data ... ","green"))
        s()
        print(colored("Well That Was QUICK","green"))
    elif arg == "sethupo":
        print(colored("deletion thingy ... ","green"))
        d()
        print(colored("Well That Was QUICK","green"))



    else:
        print(colored("there is no such command like that ","red"))
        help()


main()
    
