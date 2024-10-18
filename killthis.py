import psutil,time,os,sys
from colorama import just_fix_windows_console
from termcolor import colored
just_fix_windows_console()

# get search promt argument
arg_list = sys.argv
arg_list.remove(arg_list[0])
arg_str = ""
for arg in arg_list:
    arg_str += str(arg) + " "
arg_str = arg_str.strip()

if len(arg_list) == 0:
    print(colored("Usage: ","green") + "killthis [search process to kill]\n" + colored("Example: ","green") + "killprocess python\nSearch by ANY process and kill it EASILY!\nkillthis *  to list all processes")
elif arg_str == "--help":
    print(colored("Usage: ","green") + "killthis [search process to kill]\n" + colored("Example: ","green") + "killprocess python\nSearch by ANY process and kill it EASILY!\nkillthis *  to list all processes")
else:
    # search
    results = []
    already_added_names = []
    all_the_same = True
    found = False

    for process in psutil.process_iter():

        if process.pid != os.getpid(): #dont add own process
            if str(arg_str).lower().replace("_","").replace(".exe","").replace("*","") in str(process.name()).lower().replace("_","").replace("*",""):

                if len(results) == 0:
                    all_the_same = True
                    results.append(process)
                    already_added_names.append(process.name())
                else:
                    if not process.name() in already_added_names:
                        all_the_same = False
                    results.append(process)
                found = True


    # handle results
    if found == True:
        if all_the_same == True:
            kill_yes_or_no = input(colored("Do you want to kill: ","red") + colored(results[0].name(),"light_green") + " (" + colored("y","green") + "/" + colored("n","red") + ") ? ")
            if kill_yes_or_no == "y" or kill_yes_or_no == "yes" or kill_yes_or_no == "Y":
                if len(results) == 1:
                    results[0].kill()
                    print(colored("Killed: ","red") + colored(results[0].name(),"light_green"))
                else:
                    for process in results:
                        try:process.kill()
                        except:pass
                    print(colored("Killed: ","red") + colored(f"{results[0].name()} ({str(len(results)+1)})","light_green"))
        else:
            print(colored(f"Found {len(results)} processes. Which one to kill?","green"))
            print("──────────────────────────────────────")
            for index,process in enumerate(results):
                print(colored(f"{index+1}: ","yellow") + colored(f"{process.name()}","light_green"))

            if arg_str != "*":
                print("\n")
                kill_chooser = str(input(colored("Kill process (number or *) : ")))

                if kill_chooser == "*":
                    for process in results:
                        try:process.kill()
                        except:pass
                        print(colored("Killed: ","red") + colored(f"{process.name()}","light_green"))
                elif int(kill_chooser) >= 1 and int(kill_chooser) <= len(results)+1:
                    results[int(kill_chooser)-1].kill()
                    print(colored("Killed: ","red") + colored(f"{results[int(kill_chooser)-1].name()}","light_green"))
                

    else:
        print(colored("No process found for: ", "red") + colored(f"{arg_str}","light_red"))