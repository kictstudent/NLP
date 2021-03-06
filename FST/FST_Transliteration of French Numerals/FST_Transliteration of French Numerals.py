# import the fst module
from nltk.draw import *
from nltk.nltk_contrib.fst.fst import *

#import the tkinter module
import tkinter
from tkinter import *


# Function that handles events in the GUI
def french_numerals_now(event):
    num = int(numEntry.get())                    
    f = french_count()
    if num:
        out = str(" ".join(f.transduce(prepare_input(num))))
    sumEntry.delete(0,"end")
    sumEntry.insert(0,out)


# FST class with recognize function
class myFST(FST):
    def recognize(self, iput, oput):

        # insert your codes here
        # self.inp = iput.split()
        # self.outp = oput.split()
        self.inp = list(iput)
        self.outp = list(oput)
        # f.transduce("abc")

        if list(oput) == f.transduce(list(iput)):
            # print(" ".join(f.transduce(iput.split())))
            return True
        else:
            return False


# To make sure input is from 0-100 only
def prepare_input(integer):
    assert isinstance(integer, int) and 100 >= integer >= 0, \
        "Integer out of bounds"
    return list(f'{integer:03d}')


# Inputs number into fst and changes it to french numerals 
def french_count():
    f = myFST('french_transliteration')

    french_numerals = {0: "zero", 1: "un", 2: "deux", 3: "trois", 4: "quatre", 5: "cinq", 6: "six", 7: "sept",
                       8: "huit",
                       9: "neuf", 10: "dix", 11: "onze", 12: "douze", 13: "treize", 14: "quatorze", 15: "quinze",
                       16: "seize",
                       20: "vingt", 30: "trente", 40: "quarante", 50: "cinquante", 60: "soixante", 100: "cent"}
    french_and = 'et'

    # add the states in the FST
    for i in range(1, 11):
        f.add_state(str(i))  # add states '1' .. '10'

    # add initial state
    f.initial_state = '1'  # -> 1

    # hundreds
    for i in range(1):
        f.add_arc('1', '2', [str(i)], ())
    for i in range(1, 2):
        f.add_arc('1', '9', [str(i)], [french_numerals[100]])

    # tens
    for i in range(10):
        if i == 0:
            f.add_arc('2', '3', [str(i)], ())
        if i == 1:
            f.add_arc('2', '5', [str(i)], ())
        if 1 < i < 7:
            f.add_arc('2', '6', [str(i)], [french_numerals[i * 10]])
        if i == 7:
            f.add_arc('2', '7', [str(i)], [french_numerals[60]])
        if i == 8:
            f.add_arc('2', '8', [str(i)], [french_numerals[4]] + [french_numerals[20]])
        if i == 9:
            f.add_arc('2', '5', [str(i)], [french_numerals[4]] + [french_numerals[20]])

    # ten's place when hundred's place was 1
    for i in range(1):
        if i == 0:
            f.add_arc('9', '10', [str(i)], ())

    # ones
    # state 10-->4
    for ii in range(1):
        if ii == 0:
            f.add_arc('10', '4', [str(ii)], ())
    # state 3-->4
    for ii in list(range(0, 10)):
        f.add_arc('3', '4', [str(ii)], [french_numerals[ii]])
    # state 5-->4
    for i in range(10):
        if i < 7:
            f.add_arc('5', '4', [str(i)], [french_numerals[10 + i]])
        else:
            f.add_arc('5', '4', [str(i)], [french_numerals[10]] + [french_numerals[i]])
    # state 6-->4
    for i in range(10):
        if i == 0:
            f.add_arc('6', '4', [str(i)], ())
        if i == 1:
            f.add_arc('6', '4', [str(i)], [french_and] + [french_numerals[i]])
        if i > 1:
            f.add_arc('6', '4', [str(i)], [french_numerals[i]])
    # state 7-->4
    for i in range(10):
        if i == 1:
            f.add_arc('7', '4', [str(i)], [french_and] + [french_numerals[10 + i]])
        elif 1 < i < 7:
            f.add_arc('7', '4', [str(i)], [french_numerals[10 + i]])
        elif i == 0:
            f.add_arc('7', '4', [str(i)], [french_numerals[10 + i]])
        else:
            f.add_arc('7', '4', [str(i)], [french_numerals[10]] + [french_numerals[i]])
    # state 8-->4
    for ii in list(range(0, 10)):
        if ii == 0:
            f.add_arc('8', '4', [str(ii)], ())
        else:
            f.add_arc('8', '4', [str(ii)], [french_numerals[ii]])

    # add final/accepting state
    f.set_final('4')  # 4 ->
    return f

    
if __name__ == '__main__':

#root = Tk() until root.mainloop() is for the GUI
    root = Tk()
    root.title("French Numerals Transliteration")
    
    #These two lines can be added to add a label, but their rows should be adjusted
    #    Label(root, text="Enter input: ").grid(row=2,sticky=S, padx=4)
    #    Label(root, text="Output here").grid(row=1)
    
    numEntry = Entry(root)
    numEntry.grid(row=3, sticky=N, padx=4)

    equalButton = Button(root,text="Enter")
    equalButton.bind("<Button-1>", french_numerals_now)
    equalButton.grid(row=4)

    sumEntry = Entry(root)
    sumEntry.grid(row=5)

    root.mainloop()

string_input = input("Enter input: ")
user_input = int(string_input)
f = french_count()
if string_input:
    var = "".join(str(user_input) + '-->' + " ".join(f.transduce(prepare_input(user_input))))

# To print output(var) into output file
saveFile = open('French-trans.dat', 'w')
saveFile.write(var)
saveFile.close()

