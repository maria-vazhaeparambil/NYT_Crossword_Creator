dim = 15 #fill in grid dimension here

import pandas 
import os
import numpy as np
import math
import random
from tkinter import *
from tkmacosx import Button
import numpy as np
import copy

def solved(cross):
    ret = -1
    minimum = len(alphabet) + 1
    pick = []
    for r in range(len(cross)):
        for c in range(len(cross[r])):
            if isinstance(cross[r][c], list):
                if len(cross[r][c]) < minimum:
                    minimum = len(cross[r][c])
                    ret = [r, c]
    return ret

def impossible(cross, rposs, cposs, check_word):
    for r in range(len(cross)):
        for c in range(len(cross[r])):
            if isinstance(cross[r][c], list):
                if len(cross[r][c]) < 1:
                    return True
                rstart = check_word[r][c][0][0]
                if len(rposs[rstart][c]) < 1:
                    return True
                cstart = check_word[r][c][1][0]
                if len(cposs[r][cstart]) < 1:
                    return True
    return False

def update(cross, rposs, cposs, check_word):
    for rp in range(len(rposs)):
        for cp in range(len(rposs[rp])):
            if isinstance(cross[rp][cp], list) and len(cross[rp][cp]) == 1:
                cross[rp][cp] = cross[rp][cp][0]
                rstart = check_word[rp][cp][0][0]
                rposs[rstart][cp] = [word for word in rposs[rstart][cp] if str(word)[rp - rstart] == cross[rp][cp]] 
                if len(rposs[rstart][cp]) < 1:
                    return False, cross, rposs, cposs
                cstart = check_word[rp][cp][1][0]
                cposs[rp][cstart] = [word for word in cposs[rp][cstart] if str(word)[cp - cstart] == cross[rp][cp]] 
                if len(cposs[rp][cstart]) < 1:
                    return False, cross, rposs, cposs
                
    for rp in range(len(rposs)):
        for cp in range(len(rposs[rp])):
            if isinstance(cross[rp][cp], list) and rposs[rp][cp] != [-1] and len(rposs[rp][cp]) == 1:
                start = check_word[rp][cp][0][0]
                end = check_word[rp][cp][0][1]
                for p in range(start, end + 1):
                    cstart = check_word[p][cp][1][0]
                    cross[p][cp] = rposs[rp][cp][0][p - start]
                    if cposs[p][cstart] != [-1]:
                        cposs[p][cstart] = [word for word in cposs[p][cstart] if str(word)[cp - cstart] == cross[p][cp]]
                        if len(cposs[p][cstart]) < 1:
                            return False, cross, rposs, cposs
    
    for rp in range(len(cposs)):
        for cp in range(len(cposs[rp])):
            if cross[rp][cp] != '-1' and isinstance(cross[rp][cp], list) and cposs[rp][cp] != [-1] and len(cposs[rp][cp]) == 1:
                start = check_word[rp][cp][1][0]
                end = check_word[rp][cp][1][1]
                for p in range(start, end + 1):
                    rstart = check_word[rp][p][0][0]
                    cross[rp][p] = cposs[rp][cp][0][p - start]
                    if rposs[rstart][p] != [-1]:
                        rposs[rstart][p] = [word for word in rposs[rstart][p] if str(word)[rp - rstart] == cross[rp][p]]
                        if len(rposs[rstart][p]) < 1:
                            return False, cross, rposs, cposs
                    
    for r in range(dim):
        for c in range(dim):
            if cross[r][c] != '-1' and isinstance(cross[r][c], list):
                start_row = check_word[r][c][0][0]
                end_row = check_word[r][c][0][1]
                start_col = check_word[r][c][1][0]
                end_col = check_word[r][c][1][1]
                
                for letter in alphabet:
                    row_test = [word for word in rposs[start_row][c] if str(word)[r - start_row] == letter]
                    col_test = [word for word in cposs[r][start_col] if str(word)[c - start_col] == letter]
                    if (len(row_test) == 0 or len(col_test) == 0) and letter in cross[r][c]:
                        cross[r][c].remove(letter)  
                    
    return True, cross, rposs, cposs

def create():

    crossword = []
    for r in range(dim):
        row = []
        for c in range(dim):
            if button[r][c].cget('text') == '':
                row.append(alphabet.copy())
            else:
                row.append(button[r][c].cget('text'))
        crossword.append(row)
    
    number = []
    check_word = []
    rposs = []
    cposs = []
    for r in range(dim):
        row_num = []
        row_cw = []
        row_r = []
        row_c = []
        for c in range(dim):
            row_num.append(None)
            row_cw.append([])
            row_r.append([-1])
            row_c.append([-1])
        number.append(row_num)
        check_word.append(row_cw)
        rposs.append(row_r)
        cposs.append(row_c)
    
    count = 1
    for r in range(dim):
        for c in range(dim):
            if (r == 0 or c == 0 or crossword[r - 1][c] == '-1' or crossword[r][c - 1] == '-1') and crossword[r][c] != '-1':
                number[r][c] = count
                count += 1
    number = np.rot90(np.fliplr(number))
    
    for r in range(dim):
        for c in range(dim):
            if crossword[r][c] != '-1':
                start_row = r - 1
                while start_row > -1 and crossword[start_row][c] != '-1':
                    start_row -= 1
                start_row += 1
                end_row = r + 1
                while end_row < dim and crossword[end_row][c] != '-1':
                    end_row += 1
                end_row -= 1

                start_col = c - 1
                while start_col > -1 and crossword[r][start_col] != '-1':
                    start_col -= 1
                start_col += 1
                end_col = c + 1
                while end_col < dim and crossword[r][end_col] != '-1':
                    end_col += 1
                end_col -= 1

                if (check_word[r][c] == []):
                    check_word[r][c].append([start_row, end_row])
                    check_word[r][c].append([start_col, end_col])


    for r in range(dim):
        for c in range(dim):           
            if crossword[r][c] != '-1' and isinstance(crossword[r][c], list):
                start_row = check_word[r][c][0][0]
                end_row = check_word[r][c][0][1]
                start_col = check_word[r][c][1][0]
                end_col = check_word[r][c][1][1]

                if rposs[start_row][c] == [-1]:
                    rposs[start_row][c] = [word for word in words if len(str(word)) == end_row - start_row + 1]

                    for i in range(start_row, end_row + 1):
                        if not isinstance(crossword[i][c], list):
                            rposs[start_row][c] = [word for word in rposs[start_row][c] if str(word)[i - start_row] == crossword[i][c]]  
                        else:
                            for x in rposs[start_row][c]:
                                if str(x)[i - start_row] not in crossword[i][c]:
                                    rposs[start_row][c].remove(x)


                if cposs[r][start_col] == [-1]:
                    cposs[r][start_col] = [word for word in words if len(str(word)) == end_col - start_col + 1]
                    for i in range(start_col, end_col + 1):
                        if not isinstance(crossword[r][i], list):
                            cposs[r][start_col] = [word for word in cposs[r][start_col] if str(word)[i - start_col] == crossword[r][i]]
                        else:
                            for x in cposs[r][start_col] :
                                if str(x)[i - start_col] not in crossword[r][i]:
                                    cposs[r][start_col].remove(x)

    for r in range(dim):
        for c in range(dim):  
            if crossword[r][c] != '-1' and isinstance(crossword[r][c], list):
                start_row = check_word[r][c][0][0]
                end_row = check_word[r][c][0][1]
                start_col = check_word[r][c][1][0]
                end_col = check_word[r][c][1][1]

                for let in alphabet:
                    row_test = [word for word in rposs[start_row][c] if str(word)[r - start_row] == let]
                    col_test = [word for word in cposs[r][start_col] if str(word)[c - start_col] == let]
                    if (len(row_test) == 0 or len(col_test) == 0) and let in crossword[r][c]:
                        crossword[r][c].remove(let)
    
    works, crossword, rposs, cposs = update(crossword, rposs, cposs, check_word)

    stack = []
    pck = solved(crossword)

    count = 0
    status = ""
    
    while pck != -1:

        if not works or impossible(crossword, rposs, cposs, check_word):
            if len(stack) == 0:
                status = "impossible"
                break
            backtrack = stack.pop()
            crossword = backtrack[3]
            rposs = backtrack[4]
            cposs = backtrack[5]
            br = backtrack[0]
            bc = backtrack[1]
            crossword[br][bc].remove(backtrack[2])
            while len(stack) > 0 and len(crossword[br][bc]) == 0:
                b = stack.pop()
                crossword = b[3]
                rposs = b[4]
                cposs = b[5]
                br = b[0]
                bc = b[1]
                crossword[br][bc].remove(b[2])

            if len(stack) == 0 and len(crossword[br][bc]) == 0:
                status = "impossible"
                break

            pck = solved(crossword)

        count += 1

        let = random.choice(crossword[pck[0]][pck[1]])     
        stack.append([pck[0], pck[1], let, copy.deepcopy(crossword), copy.deepcopy(rposs), copy.deepcopy(cposs)])

        crossword[pck[0]][pck[1]] = let
        
        rstart = check_word[pck[0]][pck[1]][0][0]
        rposs[rstart][pck[1]] = [word for word in rposs[rstart][pck[1]] if str(word)[pck[0] - rstart] == let] 

        cstart = check_word[pck[0]][pck[1]][1][0]
        cposs[pck[0]][cstart] = [word for word in cposs[pck[0]][cstart] if str(word)[pck[1] - cstart] == let] 

        if len(rposs[rstart][pck[1]]) < 1 or len(cposs[pck[0]][cstart]) < 1:
            works = False
        else:
            works, crossword, rposs, cposs = update(crossword, rposs, cposs, check_word)
            pck = solved(crossword)
            
    for c in range(dim):
        for r in range(dim):
            if button[r][c].cget('bg') != 'black':
                if status == 'impossible':
                    button[r][c].configure(bg = 'red')
                    labels[r][c].configure(bg = 'red')
                else:
                    button[r][c].configure(text = crossword[r][c], bg = 'white')
                if number[r][c] != None:
                    labels[r][c].config(text=str(number[r][c]))

    if status != 'impossible':
        T1.insert(END, "DOWN\n")
        T2.insert(END, "ACROSS\n")
        for c in range(dim):
            for r in range(dim):
                if rposs[r][c][0] != -1:
                    df = (data.loc[data['answer'] == rposs[r][c][0]]).sample(1)['clue']
                    T2.insert(END, str(number[r][c]) + ". " + df.values[0] + "\n")
                if cposs[r][c][0] != -1:
                    df = (data.loc[data['answer'] == cposs[r][c][0]]).sample(1)['clue']
                    T1.insert(END, str(number[r][c]) + ". " + df.values[0] + "\n")
                    
def up(event):
    global selectedc
    if selectedc != 0:
        selectedc -= 1
    if button[selectedr][selectedc + 1].cget('text') != '-1':
        button[selectedr][selectedc + 1].configure(bg = 'white')
        labels[selectedr][selectedc + 1].configure(bg = 'white')
    if button[selectedr][selectedc].cget('text') != '-1':
        button[selectedr][selectedc].configure(bg = 'darkgoldenrod1')
        labels[selectedr][selectedc].configure(bg = 'darkgoldenrod1')

def down(event):
    global selectedc
    if selectedc != dim - 1:
        selectedc += 1
    if button[selectedr][selectedc - 1].cget('text') != '-1':
        button[selectedr][selectedc - 1].configure(bg = 'white')
        labels[selectedr][selectedc - 1].configure(bg = 'white')
    if button[selectedr][selectedc].cget('text') != '-1':
        button[selectedr][selectedc].configure(bg = 'darkgoldenrod1')
        labels[selectedr][selectedc].configure(bg = 'darkgoldenrod1')

def left(event):
    global selectedr
    if selectedr != 0:
        selectedr -= 1
    if button[selectedr + 1][selectedc].cget('text') != '-1':
        button[selectedr + 1][selectedc].configure(bg = 'white')
        labels[selectedr + 1][selectedc].configure(bg = 'white')
    if button[selectedr][selectedc].cget('text') != '-1':
        button[selectedr][selectedc].configure(bg = 'darkgoldenrod1')
        labels[selectedr][selectedc].configure(bg = 'darkgoldenrod1')

def right(event):
    global selectedr
    if selectedr != dim - 1:
        selectedr += 1
    if button[selectedr - 1][selectedc].cget('text') != '-1':
        button[selectedr - 1][selectedc].configure(bg = 'white')
        labels[selectedr - 1][selectedc].configure(bg = 'white')
    if button[selectedr][selectedc].cget('text') != '-1':
        button[selectedr][selectedc].configure(bg = 'darkgoldenrod1')
        labels[selectedr][selectedc].configure(bg = 'darkgoldenrod1')
    
def button_click(r, c):
    global selectedr 
    global selectedc
    if button[selectedr][selectedc].cget('text') != '-1':
        button[selectedr][selectedc].configure(bg = 'white')
        labels[selectedr][selectedc].configure(bg = 'white')
    selectedr = r
    selectedc = c
    if button[r][c].cget('text') != '-1':
        button[r][c].configure(bg = 'darkgoldenrod1')
        labels[r][c].configure(bg = 'darkgoldenrod1')

def reset():
    T1.delete("1.0","end")
    T2.delete("1.0","end")
    for r in range(dim):
        for c in range(dim):
            button[r][c].config(text = "", bg = 'white')
            labels[r][c].config(text = "", bg = 'white')
    
def deleted(ev):
    button[selectedr][selectedc].config(text = '', bg = 'darkgoldenrod1')
    labels[selectedr][selectedc].configure(bg = 'darkgoldenrod1')
        
def select(ev, i):
    let = alphabet[i].upper()
    button[selectedr][selectedc].config(text=let)

def fill_black():
    button[selectedr][selectedc].configure(text = '-1', bg = 'black')
    labels[selectedr][selectedc].configure(bg = 'black')

def close():
    root.destroy()

alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
               'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
size = 6
box = 40
spec = 60
answ = 600
minimum = 0
shift = 5

filename = os.getcwd() + '/crosswords/clues.tsv'
data=pandas.read_csv(filename,sep='\t')[1:]
data = data[~data['clue'].str.contains("-Across", na=False)]
data = data[~data['clue'].str.contains("-Down", na=False)]

ls = list(data['answer'].values)
strs = []
for w in ls:
    if isinstance(w, str):
        strs.append(w)
ls = sorted(strs)
prev = ""
count = 0
words = []
for w in ls:
    if w == prev:
        count += 1
    else:
        if count >= minimum:
            words.append(prev)
        prev = w
        count = 1

selectedr = 0
selectedc = 0

labels = []
button = []
for r in range(dim):
    row_b = []
    row_l = []
    for c in range(dim):
        row_b.append(None)
        row_l.append(None)
    button.append(row_b)
    labels.append(row_l)

root = Tk()
root.title("Crossword")
root.configure(background='white')

frame = Frame(root, bg = 'white')

root.bind('<Left>', left)
root.bind('<Right>', right)
root.bind('<Up>', up)
root.bind('<Down>', down)
root.bind('<BackSpace>', deleted)

for i in range(len(alphabet)):
    def make_lambda(x):
        return lambda ev:select(ev,x)
    root.bind(alphabet[i].lower(), make_lambda(i))

for r in range(dim):
    for c in range(dim):
        button[r][c] = Button(root, text ="",  bg = 'white', command = lambda r=r, c=c: button_click(r, c))
        button[r][c].config(height = box, width = box)
        button[r][c].place(x=r*box,y=c*box)
        labels[r][c] = Label(root, text="", font=("TkDefaultFont", size), bg='white')
        labels[r][c].place(x=r*box+shift, y=c*box+shift)

blck = Button(root, text ="Black",  command=fill_black, bg = 'white')
blck.config(height = box, width = spec)
blck.place(x=(dim * box)/2 - 3 * spec/2,y=box * dim)

rst = Button(root, text ="Reset", command=reset, bg = 'white')
rst.config(height = box, width = spec)
rst.place(x=(dim * box)/2 - spec/2,y=box * dim)

crt = Button(root, text ="Create", command=create, bg = 'white')
crt.config(height = box, width = spec)
crt.place(x=(dim * box)/2 + spec/2,y=box * dim)


scrollo = Scrollbar(root, orient='vertical')
scrollo.pack(side=RIGHT, fill = Y)
T1 = Text(root, width = 40, height = (dim + 1) * box, yscrollcommand=scrollo.set)
T1.pack(side=RIGHT)
T1['yscrollcommand'] = scrollo.set

scrollt = Scrollbar(root, orient='vertical')
scrollt.pack(side=RIGHT, fill = Y)
T2 = Text(root, width = 40, height = (dim + 1) * box, yscrollcommand=scrollt.set)
T2.pack(side=RIGHT)
T2['yscrollcommand'] = scrollt.set

root.protocol("WM_DELETE_WINDOW", close)
root.geometry(str(dim * box + answ + shift) + "x" + str((dim + 1) * box))

root.mainloop()