# !/usr/bin/python27
# ~/.conkycolor/

"""
Sorry for my bad English :)
This script's written to add "Note" function to conky 
Used to interact with note in commandline(terminal) using conky
conkycolors: https://github.com/helmuthdu/conky_colors is recommended to config conky easier
Written by Messorem: https://github.com/m3ss0r3m/
Version 2
"""

import sys
import getopt
import subprocess
import re

def usage():
    print "Note script for conky"
    print "Written by Messorem"
    print "V2"
    print
    print "-------------------------------------------------------------------------------"
    print "Usage: note [OPTION] [-i|--index= <index>] CONTENTS"
    print
    print "OPTION:"
    print
    print "-h, --help"
    print "      display help and exit"
    print "-a, --add <content> [index with -i option]"
    print "      adding content to current page"
    print "-r, --remove [content]|[index with -i option]"
    print "      remove content of current page"
    print "-c, --create [index with -i option]"
    print "      create new page"
    print "-d, --delete [index with -i option]"
    print "      delete page"
    print "-t, --turn [next|pre]|[index with -i option]"
    print "      turn page"
    print "         next: next page"
    print "         pre|previous: previous page"
    print "-o, --open [<editor>]"
    print "      open notes file (default : gedit)"
    print "--info"
    print "      show current page number"
    print "<index> : line number (of current page) or page number, depend on used [OPTION]"
    print "----------------------------------END------------------------------------------"
    sys.exit()

class Note():
    """
    Note class to creates and interacts with note file
    We have a text file to store all of note content, and another text file contains only current page(the page is displayed on conky)
    The file displayed is current file, so all modify in note page don't be displayed on your desktop
    One page contains 13 line of note by default, but you can modify it depend on your conky config
    To do a operator with note, you need pass page number and line number to a pointer (pointer["page"] and pointer["line"])
    The first line of note file contains current status(<page_number>/<sum_of_pages>) 
    Page nummber is marked in note file: --<page_number>--
    'Current page' file has 2 tab(\t) before each line for beautiful. It depend on your conky config too 
    """
    def __init__(self):
        self.pointer = {"page" : 1, "line" : 1}
        self.notes = open('notes', 'r+')
        self.current = open('current', 'r+')
        self.data = self.notes.read().split('\n')
        self.data = self.data[:len(self.data)-1]
        self.info = self.get_info()
        #Just open file to get data, so close it now. Open it again when necessary
        self.notes.close()
        self.current.close()

    def add(self, content):
        #adding content to note file
        #using pointer["page"] and pointer["line"] to mark location of content added
        result = []
        condition = False
        for i in range(len(self.data)):
            result.append(self.data[i])
            if (self.data[i] == '--%d--'%self.pointer["page"]):
                #line pointer/number
                j = 0
                #turn on the flag
                condition = True

            if condition:
                j += 1
                if j == self.pointer["line"]:
                    result.append(content)
                    #turn off the flag
                    condition = False

        self.data = result
        self.write_data('notes', result)
        self.put_to_current()
        return 0

    def remove(self, content = ''):
        #removing content to note file
        #using pointer["page"] and pointer["line"] to mark location of content removed
        #pointer["line"] set to 0 to remove by content
        result = []
        condition = False
        for i in range(len(self.data)):
            result.append(self.data[i])

            if (self.data[i] == '--%d--'%self.pointer["page"]):
                #line pointer/number
                j = -1
                #turn on the flag
                condition = True

            if (self.data[i] == '--%d--'%(self.pointer["page"]+1)) or i == 14:
                condition = False

            if condition:
                if self.pointer["line"] != 0:
                    j += 1
                    if j == self.pointer["line"]:
                        result = result[:len(result)-1]
                else:
                    if self.data[i] == content:
                        result = result[:len(result)-1]

        self.data = result
        self.write_data('notes', result)
        self.put_to_current()
        return 0

    def create(self):
        #create new page
        #using pointer["page"] only, pointer["line"] is set to 0
        condition = False
        result = []
        j = 0
        for i in range(len(self.data)):
            if condition:
                j += 1
                if re.match('--(.*)--', self.data[i]):
                    result.append('--%d--'%(int(self.data[i].strip('-'))+1))
                elif j == self.get_max_line():
                    result.append(self.data[i])
                    result.append('--%d--'%(self.pointer["page"]+1))
                else:
                    result.append(self.data[i])
            else:
                result.append(self.data[i])

            #check the page index
            if (self.data[i] == '--%d--'%self.pointer["page"]): 
                #turn on the flag
                condition = True

        result[0] = '%d/%d'%(self.get_info()[0], self.get_info()[1]+1)

        self.data = result
        self.write_data('notes', result)
        self.notes.close()
        return 0


    def delete(self):
        #delete an exist page
        #using pointer["page"] only, pointer["line"] is set to 0
        condition1 = False
        condition2 = False
        result = []
        for i in range(len(self.data)):

            if condition1:
                if not condition2:
                    if re.match('--(.*)--', self.data[i]):
                        result.append('--%d--'%(int(self.data[i].strip('-'))-1))
                    else:
                        result.append(self.data[i])
                else:
                    if re.match('--(.*)--', self.data[i]):
                        result.append('--%d--'%(int(self.data[i].strip('-'))-1))
                        condition2 = False
            else:
                result.append(self.data[i])

            #check the page index
            if (self.data[i] == '--%d--'%self.pointer["page"]):
                #turn on 2 flag
                condition1 = True
                condition2 = True
                result = result[:len(result)-1]

        result[0] = '%d/%d'%(self.get_info()[0], (self.get_info()[1]-1))

        self.data = result
        self.write_data('notes', result)
        self.notes.close()
        return 0

    def turn_page(self):
        #just place a new page to current file :)
        #using pointer["page"] only, pointer["line"] is set to 0
        self.data[0] = '%d/%d'%(self.pointer["page"], self.get_info()[1])
        self.write_data('notes', self.data)
        self.put_to_current()

    def put_to_current(self):
        #write a page to current file for displayed
        #using pointer["page"] only, pointer["line"] is set to 0
        self.notes = open('notes', 'r+')
        self.data = self.notes.read().split('\n')
        self.data = self.data[:len(self.data)-1]
        result = []
        condition = False
        for i in range(len(self.data)):
            if condition:
                if self.data[i] == '--%d--'%(self.pointer["page"]+1):
                    self.write_data('current', result + ['\t\t'] * (13 - self.get_max_line()))
                    return 0
                result.append('\t\t' + self.data[i])
            if (self.data[i] == '--%d--'%self.pointer["page"]):
                condition = True

        self.write_data('current', (result + ['\t\t'] * (13 - self.get_max_line())))
        return 0

    def get_max_line(self):
        #return max line number of current page
        counter = 0
        condition = False
        for i in range(len(self.data)):
            if condition:
                counter += 1
                if re.match('--(.*)--', self.data[i]):
                    return (counter-1)
                elif i == (len(self.data)-1):
                    return counter
            if (self.data[i] == '--%d--'%self.pointer["page"]):
                condition = True
                if i == len(self.data) - 1:
                    return 0

    def write_data(self, file, data):
        f = open(file, 'w')
        for i in data:
            f.write(i + '\n')
        f.close()

    def get_info(self):
        #return info(status)
        self.notes = open('notes', 'r+')
        self.data = self.notes.read().split('\n')
        self.data = self.data[:len(self.data)-1]
        self.info = self.data[0].split('/')
        self.notes.close()
        return (int(self.info[0]), int(self.info[1]))


def main():
    note = Note()
    index = 0
    if not len(sys.argv[1:]):
        usage()

    # read commandline options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "harcdti:o", ["help", "add", "remove", "create", "delete", "turn", "index=", "open", "info"])
        for i in range(len(opts)):
            if opts[i][0] in ("-i", "--index="):
                temp = opts[0]
                opts[0] = opts[i]
                opts[i] = temp

        if opts[0][0] in ("-i", "--index="):
            if opts[1][0] in ("-a", "--add", "-r", "--remove"):
                index_type = 'line'
            elif opts[1][0] in ("-c", "--create", "-d", "--delete", "-t", "--turn"):
                index_type = 'page'

    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()

        elif o in ("-i", "--index") and index_type == 'line':
            if 1 <= int(a) and int(a) <= note.get_max_line():
                index = int(a)
            else:
                print "[!]Invalid line number: Line number must in 1-%s" %(note.get_max_line())
                sys.exit()

        elif o in ("-i", "--index") and index_type == 'page':
            if 1 <= int(a) and int(a) <= note.get_info()[1]:
                index = int(a)
            else:
                print "[!]Invalid page number: Page number must in 1-%s" %(note.get_info()[1])
                sys.exit()

        elif o in ("-a", "--add"):
            note.pointer["page"] = note.get_info()[0]

            if index:
                note.pointer["line"] = index
            else:
                note.pointer["line"] = note.get_max_line() + 1
                if note.pointer["line"] > 13:
                    print "[!]Current page is full to add! You need to create a new page next to current one or add to the next page!"
                    choose = raw_input("Do you want to create a new page? [Y/n]")
                    if choose in ('Y', 'y', 'yes', 'Yes', ''):
                        note.create()
                        note.pointer["page"] += 1
                        note.pointer["line"] = 1
                    elif choose in ('N', 'n', 'no', 'No'):
                        if note.pointer["page"] == note.get_info()[1]:
                            print "[!]No page left to add content. You should create a new page or add to another page."
                            print "[!]Nothing added! Exit now!"
                            sys.exit()
                        else:
                            note.pointer["page"] += 1
                            if note.get_max_line() == 13:
                                print "[!]The next page is full. You should create a new page or add to another page."
                                print "[!]Nothing added! Exit now!"
                                sys.exit()
                            else:
                                note.pointer["line"] = 1
                    else:
                        print '[!]Your choose is not recognized!'

            note.add(' '.join(args))
            note.turn_page()

        elif o in ("-r", "--remove"):
            note.pointer["page"] = note.get_info()[0]
            note.pointer["line"] = index
            if index:
                note.remove()
            else:
                note.remove(' '.join(args))

        elif o in ("-c", "--create"):
            if args:
                print "Your \"create\" command is invalid systax. Please see usage by -h or --help."
                sys.exit()

            if index:
                note.pointer["page"] = index - 1
            else:
                note.pointer["page"] = note.get_info()[0]
            note.pointer["line"] = 0
            note.create()
        
        elif o in ("-d", "--delete"):
            if args:
                print "Your \"delete\" command is invalid systax. Please see usage by -h or --help."
                sys.exit()

            note.pointer["line"] = 0
            if index != 0:
                note.pointer["page"] = index
            else:
                note.pointer["page"] = note.get_info()[0]

            while True:
                choose = raw_input("Do you want to delete page %d? [y/N] "%note.pointer["page"])
                if choose in ('Y', 'y', 'yes', 'Yes'):
                    note.delete()
                    if note.pointer["page"] > 1:
                        note.pointer["page"] -= 1
                    note.get_info()
                    note.turn_page()
                    break
                elif choose in ('N', 'n', 'no', 'No', ''):
                    sys.exit()
                else:
                    print '[!]Your choose is not recognized!'

            if index == note.get_info()[0]:
                note.put_to_current()            

        elif o in ("-t", "--turn"):
            note.pointer["line"] = 0
            if index != 0:
                note.pointer["page"] = index
            else:
                if args[0] == "next":
                    note.pointer["page"] = note.get_info()[0] + 1
                elif args[0] == "pre" or args[0] == "previous":
                    note.pointer["page"] = note.get_info()[0] - 1
                else:
                    print "[!]Turn to what? Please see usage by -h or --help."
                    sys.exit()

            if 1 <= note.pointer["page"] and note.pointer["page"] <= note.get_info()[1]:
                note.turn_page()
            else:
                print ("[!]No page left to turn!")

        elif o in ("-o", "--open"):
            note.pointer["line"] = 0
            note.pointer["page"] = note.get_info()[0]
            if not args:
                subprocess.check_output('gedit notes', stderr=subprocess.STDOUT, shell=True)
            else:
                subprocess.check_output('%s notes' %args[0], stderr=subprocess.STDOUT, shell=True)
            note.put_to_current()

        elif o in ("--info"):
            print str(note.get_info()[0]) + '/' + str(note.get_info()[1])

        else:
            assert False, "Unhandled Option"

if __name__ == "__main__":
    main()
