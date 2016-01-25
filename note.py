# !/usr/bin/python27

import sys
import getopt
import subprocess


def usage():
    print "Note script for conky"
    print "Written by m3ss0r3m"
    print
    print "---------------------------------------------------------"
    print "Usage: note [OPTION] [-i, --index] <line number> CONTENTS"
    print
    print "OPTION:"
    print
    print "-h, --help"
    print "      display help and exit"
    print "-a, --add"
    print "      adding content to task file"
    print "-r, --remove"
    print "      remove content to task file"
    print "-b, --blank"
    print "      remove all contents in task file"
    print "-o, --open [<editor>]"
    print "      open notes file (default : gedit)"
    print "--------------------------END-----------------------------"
    sys.exit()


def main():
    line_number = None
    if not len(sys.argv[1:]):
        usage()

    # read commandline options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "harbi:o", ["help", "add", "remove", "blank", "index", "open"])
        for i in range(len(opts)):
            if opts[i][0] in ("-i", "--index"):
                temp = opts[0]
                opts[0] = opts[i]
                opts[i] = temp

    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()

        elif o in ("-i", "--index"):
            f = open("notes", "r")
            max_line = len(f.read().split("\n"))
            f.close()
            if 1 <= int(a) and int(a) <= max_line:
                line_number = int(a)-1
            else:
                print "[!] Invalid line number: Line number must in 1-%s" %max_line
                sys.exit()

        elif o in ("-a", "--add"):
            if line_number == None:
                f = open("notes", "a")
                f.write(args[0] + "\n")
                f.close()
            else:
                f = open("notes", "r")
                data = f.read().split("\n")
                f.close()
                re = []
                for i in range(len(data)):
                    if i == line_number:
                        re.append(args[0])
                        re.append(data[i])
                    else:
                        re.append(data[i])
                f = open("notes", "w")
                for i in re:
                    if i != '':
                        f.write(i+"\n")
                f.close()



        elif o in ("-r", "--remove"):
            f = open("notes", "r")
            data = f.read().split("\n")
            f.close()
            re = []
            if line_number == None:
                for i in data:
                    if i.strip() != str(args[0]):
                        re.append(i)
            else:
                for i in range(len(data)):
                    if i != line_number:
                        re.append(data[i])


            f = open("notes", "w")
            for i in re:
                if i != '':
                	f.write(i+"\n")
            f.close()
        
        elif o in ("-b", "--blank"):
            f = open("notes", "w")
            f.close()

        elif o in ("-o", "--open"):
        	if not args:
        		subprocess.check_output('leafpad notes', stderr=subprocess.STDOUT, shell=True)
        	else:
        		subprocess.check_output('%s notes' %args[0], stderr=subprocess.STDOUT, shell=True)

        else:
            assert False, "Unhandled Option"

if __name__ == "__main__":
    main()
