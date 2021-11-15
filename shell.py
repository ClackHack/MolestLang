import molest, os, datetime, _thread, sys, argparse
def begin(s,r):
  return s[:len(r)]==r
print("MolestLang 0.0.0, type credits for more info")
directory="C:/Swamipp/Programs/"
def notepad(f):
    os.system("notepad.exe "+directory+f)
    return
directory="Programs/"
while 1:
    command=input(">>> ")
    if command=="exit":
        break
    elif command=="credits":
        print("Developed By ClackHack")
    elif begin(command,"file "):
        f=command.replace("file ","")
        if not f.endswith(".mol"):
            print("Expected .mol file")
            continue
        try:
            open(directory+f,"r").read()
        except:
            open(directory+f,"w").write("")
        _thread.start_new_thread(notepad,(f,))
        #os.system("notepad.exe Programs/"+f)
    elif begin(command,"run "):
        f = command.replace("run ","")
        try:
            code=open(directory+f,"r").read()
            y=datetime.datetime.now()
            result,error=molest.run(f,code)
            x=datetime.datetime.now()
            if error:
                print(error.toString(),sep="\n")
            else:
                delta=(x-y).total_seconds()
                print(f"\nExecuted with zero errors in {delta} seconds")
        except KeyboardInterrupt:
          continue
        except SyntaxError as e:
            print("Could not find file, or fatal error...",e)

    elif command=="programs":
        f=os.listdir(directory.strip("/"))
        for p in f:
            print(p)
    elif begin(command,"delete"):
        f = command.replace("delete ","").strip()
        try:
            os.remove(directory+f)
        except:
            print("The file you specified was not found...")
    elif command=="help":
        print("Commands are file, run, programs, delete, and exit\nCheck the github page for syntax support")
    else:
        print("Unkown command...\ntype help for help... ")
