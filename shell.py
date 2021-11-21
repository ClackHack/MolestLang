import molest, os, datetime, _thread, sys, argparse


parser = argparse.ArgumentParser(description="MolestLang")
parser.add_argument("file",nargs="?",type=str,help="file to be executed",default="")
args=parser.parse_args()
if args.file:
  try:
    code=open(args.file,"r").read()
    y=datetime.datetime.now()
    result,error=molest.run(args.file,code)
    x=datetime.datetime.now()
    if error:
        print(error.toString(),sep="\n")
    else:
        print(f"\nExecuted with zero errors in {(x-y).total_seconds()} seconds")
  except KeyboardInterrupt:
    sys.exit()
  except Exception as e:
    print("Could not find file, or fatal error...",e)
  sys.exit()


def begin(s,r):
  return s[:len(r)]==r
print("MolestLang 0.0.1, type credits for more info")

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
        print("Unkown command...\ntype 'help' for help... ")
