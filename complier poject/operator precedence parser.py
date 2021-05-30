from tkinter import *
from PIL import Image,ImageTk
import sys
import shlex
import csv
def Interface():
    root=Tk() # for window opening tag
    root.geometry('+%d+%d'%(1250,10))

    header = Frame(root,width=800,height=175,bg="white")
    header.grid(columnspan=3,rowspan=2,row=0)

    logo = Image.open('logo.PNG')
    logo= logo.resize((int(logo.size[0]/3),int(logo.size[1]/3)))
    logo= ImageTk.PhotoImage(logo)
    logo_label = Label(image=logo , bg="white" )
    logo_label.image = logo
    logo_label.grid(column=0,row=0,rowspan=2,sticky=NW,padx=20,pady=40)

    instruction = Label(root,text="Enter The Grammer : ",font="Raleway",bg="white")
    instruction.grid(columnspan=2,column=0,row=0,rowspan=2)

    text = Entry(text="enter the text : ")
    text.grid(column=1,row=0,rowspan=2)

    button = Button(root,text='CLICK ',command=lambda:clickfunction(text.get()),font=("shanti,5"),height=1,width=20,bg="#c8c8c8")
    button.grid(columnspan=3,column=0,row=1,rowspan=2)

    save_img= Frame(root,width=800,height=175,bg="#c8c8c8")
    save_img.grid(columnspan=3,rowspan=1,row=4)


    root.mainloop() # for window closing tag
def clickfunction(text):
    # testing of inputs
    input_string = text
    print("Input: ", input_string)

    # tokinzation.
    input_ind = list(shlex.shlex(input_string))
    input_ind.append('$')
    print()
    print("Sybmol table for above input")
    sybmolTable = {}
    # creating sybmol table
    c = 0
    for i, val in enumerate(input_ind):
        if val in ['+', '-', '*', '/','%']:
            sybmolTable[str(val)] = "<" + val + ">"
            c = c + 1
        elif val in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            sybmolTable[val] = val
        elif val not in ['$']:
            sybmolTable[str(val)] = "<" + val + ">"

    # printing Symbol Table
    print()
    print("Tokens")
    for key, value in sybmolTable.items():
        print('{:10s}'.format("|    " + str(key)), '{:10s}'.format("|    " + str(value)), '{:10s}'.format("|"))

    # Reading Grammer from grammer.txt
    master = {}
    master_list = []
    new_list = []
    non_terminals = []
    grammar = open('grammar.txt', 'r')

    for row2 in grammar:

        if '->' in row2:
            if len(new_list) == 0:
                start_state = row2[0]
                non_terminals.append(row2[0])
                new_list = []
                new_list.append(row2.rstrip('\n'))
            else:
                master_list.append(new_list)
                del new_list
                new_list = []
                new_list.append(row2.rstrip('\n'))
                non_terminals.append(row2[0])


        elif '|' in row2:
            new_list.append(row2.rstrip('\n'))

    master_list.append(new_list)

    for x in range(len(master_list)):
        for y in range(len(master_list[x])):
            master_list[x][y] = [s.replace('|', '') for s in master_list[x][y]]
            master_list[x][y] = ''.join(master_list[x][y])
            master[master_list[x][y]] = non_terminals[x]

    for key, value in master.items():
        if '->' in key:
            length = len(key)
            for i in range(length):
                if key[i] == '-' and key[i + 1] == ">":
                    index = i + 2
                    break
            var_key = key
            new_key = key[index:]

    var = master[var_key]
    del master[var_key]
    master[new_key] = var

    # reading parsing table from file /printing also done.
    order_table = []
    with open('TABEL.csv', 'r') as file2:
        order = csv.reader(file2)
        print()
        print("Table:")
        temp = 0
        for i, row in enumerate(order):
            if (i == 0):
                temp = len(row)
            order_table.append(row)
            for j, cell in enumerate(row):
                if i == 0 and j == 1:
                    print("   " + cell + " ", end="")
                elif cell == " ":
                    print("   " + " ", end="")
                else:
                    print("  " + cell + " ", end="")

            print(" ")
        # print("   ___", end="")
        # for _ in range(0, temp):
        #     print("____", end="")
        # print()
        # print()
        # print()

    operators = order_table[0]
    # printing error message if occurs.
    for val in input_ind:
        if val not in operators:
            popupmsg("Rejected!")

    # Here starts the whole parsing and steps are also shown
    # in output with awesome UI
    stack = []
    stack.append('$')
    # print()
    # print(
    #     "__________________________________________________________________________________________________________________________________________________________________")
    # print("                                                                        Syntax Analysis")
    # print(
    #     "__________________________________________________________________________________________________________________________________________________________________")
    # print('{:50s}'.format("   Stack"), '{:70s}'.format("Input"), '{:25s}'.format("Precedence relation"),
    #       '{:8s}'.format("Action"))

    error = ""
    vlaag = 1
    while vlaag:

        if input_ind[0] == '$' and len(stack) == 2:
            vlaag = 0
        elif input_ind[0] == '$' and (len(stack) == 3):
            vlaag = -1
        elif len(input_ind) == 2:
            if '+' in input_ind:
                vlaag = -1
            if '-' in input_ind:
                vlaag = -1
            if '*' in input_ind:
                vlaag = -1
            if '/' in input_ind:
                vlaag = -1
            error = error + "Operator at the end of expression"

        length = len(input_ind)

        buffer_inp = input_ind[0]

        if (buffer_inp in ['+', '-', '/', '*'] and stack[len(stack) - 1] in ['+', '-', '/', '*']) or input_string[
            0] in ['+', '-', '/', '*']:
            vlaag = -1
            if input_string[0] in ['+', '-', '/', '*']:
                error = error + "Operator at Start"
            else:
                error = error + "Two Operators together"

        temp1 = operators.index(str(buffer_inp))
        # print("   stack", stack, stack[-1])
        if stack[-1] in non_terminals:
            buffer_stack = stack[-2]
        else:
            buffer_stack = stack[-1]
        temp2 = operators.index(str(buffer_stack))

        precedence = order_table[temp2][temp1]

        if precedence == '<':
            action = 'shift'
        elif precedence == '>':
            action = 'reduce'

        # print('{:50s}'.format("   " + str(stack)), '{:70s}'.format(str(input_ind)),
        #       '{:25s}'.format("      " + precedence), '{:8s}'.format(action))

        if action == 'shift':
            stack.append(buffer_inp)
            input_ind.remove(buffer_inp)
        elif action == 'reduce':
            for key, value in master.items():
                var1 = ''.join(stack[-1:])
                var2 = ''.join(stack[-3:])
                if str(key) == str(buffer_stack):
                    stack[-1] = value
                    break
                elif key == var1 or stack[-3:] == list(var1):
                    stack[-3:] = value
                    break
                elif key == var2:
                    stack[-3:] = value
        del buffer_inp, temp1, buffer_stack, temp2, precedence

        # final conditions which also does error checking
        if vlaag == 0:
            print("\n")
            popupmsg("Accepted!")
        elif vlaag == -1:
            popupmsg("Rejected!")
            return

    return
def popupmsg(msg):
    popup = Tk()
    popup.wm_title("!")
    label = Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()
Interface()