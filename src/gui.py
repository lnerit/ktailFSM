#!/usr/bin/python
import sys
import os.path
from Tkconstants import END, WORD, FALSE, HORIZONTAL, BOTTOM, X, VERTICAL,\
    RIGHT, Y, BOTH, LEFT, W
from ktail import kTailFSMGraph
import logging



sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import Tkinter as tk
import ttk
from tkFileDialog import askopenfilename
from ScrolledText import *
from Tkinter import  Canvas, PhotoImage, StringVar, Label, Scrollbar,\
Listbox, Checkbutton, IntVar, TclError
import tkMessageBox

win = tk.Tk() 
win.title("K-TAIL FINITE STATE AUTOMATA")
win.resizable(width=FALSE, height=FALSE)
    
fileName=StringVar()
stateAlias=StringVar()
traces=StringVar()
traceholder=[]
kvalue=None
columns = []
loadEquivalentState=[]
stateAliasMapList={}

def __init__(self,param):
    self.log=logging.getLogger('gui.py')
    
def fileOpen():
    try:
        #win.withdraw() # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename(filetypes=(("Text Files",".txt"),("All Files","*.*"))) # show an "Open" dialog box and return the path to the selected file
        if filename!=None:
            print(filename)
            fName.delete(0, 'end')
            fName.insert(0, filename)
        else:
            pass
    except IOError:
        tkMessageBox.showerror("Error", "Error opening log file")
      
def importTraces():
        #Import Traces from file and display on textPad
        try:
            contents=[]
            textPad.delete('1.0', END) #clear the textbox before loading traces
            with open(fName.get(), 'r') as my_file:
                for line in my_file:
                    #contents.append(line.rstrip().split(','))
                    line=line.strip()
                    contents.append(line)
                
            for row in contents:
                textPad.insert(0.0, row)   
        except IOError:
            tkMessageBox.showinfo("IOError", IOError.message)
  
        
        
def text_FromTextBox(txtPad):
        columns[:] = [] #clear existing items in the list
        for line in txtPad:
                    try:
                        line=line.strip()
                        columns.append(str(line))
                    except IndexError: pass # if the line doesn't have n columns
        return str(columns)
     
def generateAutomata():
        import time
        start_time=time.time()
        if len(textPad.get('1.0',END))==0 or len(textPad.get('1.0',END))==1:
            tkMessageBox.showinfo("Empty trace","The trace is empty.Please select a trace log.")
            return
        try:
            text_FromTextBox(textPad.get('1.0', END).split(','))
            statsPad.configure(state='normal')
            loadEquivalentState=loadStatsLogToTextBox(int(box.get()),columns)

            #load image to canvas
            loadFSMImage()
            #print 'statemap called from GUI'+str(kTailFSMGraph.stateMap)
            stateMapCopy=kTailFSMGraph.stateMap.copy()
            #replace the embedded dictionary (states) keys with the state alias
            
            #Check if the checkbox is checked or not
            if int(var1.get())==0:
                loadStateAliasToListBox(kTailFSMGraph.getUniqueStates, listBox)
                
            #We iterate throug the stateamp dictionary replace each state keys with the alias names
            print("--- %s seconds ---" % (time.time() - start_time))
            for k,v in stateMapCopy.items():
                print k,v   
            aliasDict={}
            for s in kTailFSMGraph.getUniqueStates:
                aliasDict[s]={}
            print aliasDict
            
        except "Error":
            print 'Error'
        print 'Generate Automata'
        
def kValueSelectormethod (self):
        print("method is called")
        
#If there is no image file ktail.png, then create a blank image file to draw the transition graph       
def generateNewImage(self):
        from PIL import Image
        my_list=[]
        img = Image.new('RGB', (255, 255))
        img.putdata(my_list)
        try:
            img.save('../graph/ktail.png')
        except IOError:
            tkMessageBox.showerror("File Error", "Error occured while saving image file")
    
#item=None
 
def loadFSMImage():
        try:
            img = PhotoImage(file="../graph/ktail.png")
            label.image = img # keep a reference!
            imgWidth1 = canvas.winfo_width()
            imgHeight1 =canvas.winfo_height()
            x = (imgWidth1)/2.0
            y = (imgHeight1)/2.0
            #item = canvas.create_image(x, y, anchor=tk.CENTER,image=img,tags="bg_img") # <--- Save the return value of the create_* method.
            canvas.create_image(x, y, anchor=tk.CENTER,image=img,tags="bg_img")
        except TclError:
            generateNewImage
        return
    
def loadStateAliasToListBox(lst,Listbox):
    Listbox.delete(0, END)
    for item in lst:
        Listbox.insert(END, item)
        #We initialise the dictionary with the with alias with the original states
        stateAliasMapList[item]={item}
    
def set_list(self):
    try:
        index=listBox.curselection()[0]
        #delete the old listbox line
        listBox.delete(index)
        
    except IndexError:
        index=tk.END
    listBox.insert(index, sAlias.get())
    stateAliasMapList[index]= sAlias.get()

def closeWindow():
    win.destroy()
            
def configRowCol(objectx,weight):
    objectx.rowconfigure(0,weight=weight)
    objectx.columnconfigure(0,weight=weight)
    return objectx

def configGrid(objectx,col,row,colspan,rowspan):
    objectx.grid(column=col,row=row,rowspan=rowspan, columnspan=colspan, sticky=(tk.N, tk.S, tk.W, tk.E))
    return objectx

def setScrollBar(canvas,frame):
    hbar=Scrollbar(frame,orient=HORIZONTAL)
    hbar.pack(side=BOTTOM,fill=X)
    hbar.config(command=canvas.xview)
    vbar=Scrollbar(frame,orient=VERTICAL)
    vbar.pack(side=RIGHT,fill=Y)
    vbar.config(command=canvas.yview)
    #canvas.config(width=400,height=400)
    canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    canvas.pack(side=LEFT,expand=True,fill=BOTH)
    
#Add canvas frame for canvas area to draw image
#stateDiagramFrame=ttk.Frame(win,text='Finite State Automata',width=400,height=400)
stateDiagramFrame=ttk.Frame(win,width=400,height=500)
#stateDiagramFrame.grid(column=0,row=0,rowspan=1, columnspan=1, sticky=(tk.N, tk.S, tk.W, tk.E))
configGrid(stateDiagramFrame,0,0,1,1)
configRowCol(stateDiagramFrame,50)

#Build LabelFrame for the objects on the GUI
objFrame=ttk.LabelFrame(win,text='Trace Input')
#objFrame.grid(column=0,row=1,rowspan=1, columnspan=1,sticky=(tk.N, tk.S, tk.W, tk.E))
configGrid(objFrame,0,1,1,1)
configRowCol(objFrame,1)

statsFrame=ttk.LabelFrame(win,text='K-Tails Log Information...',width=50,height=100)
#statsFrame.grid(column=0,row=2,rowspan=1, columnspan=1, sticky=(tk.N, tk.S, tk.W, tk.E))
configGrid(statsFrame,0,2,1,1)
configRowCol(statsFrame,1)
#Add a frame for the stats display text area
statsTextDisplayFrame=ttk.LabelFrame(statsFrame,text='DisplayLog...',width=50,height=100)
#statsTextDisplayFrame.grid(column=0,row=2,rowspan=1, columnspan=1, sticky=(tk.N, tk.S, tk.W, tk.E))
configGrid(statsTextDisplayFrame,0,2,1,1)
configRowCol(statsTextDisplayFrame,1)

btnStatsFrame=ttk.LabelFrame(statsFrame,text='---') 
#btnStatsFrame.grid(column=1,row=2)
configGrid(btnStatsFrame,1,2,1,1)
configRowCol(btnStatsFrame,1)

var1 = IntVar()
ck=Checkbutton(btnStatsFrame, text="State Alias", variable=var1)
ck.pack(side=tk.TOP, anchor=tk.S, expand=tk.YES)

#Add a button to close the window inside the tab
try:
    photo1 = tk.PhotoImage(file="../icon/dialog_cancel.png")
    btnClose=ttk.Button(btnStatsFrame,text="Close window",image=photo1,command=closeWindow,width=15)
    btnClose.pack(side=tk.BOTTOM,anchor=tk.N,fill=BOTH)
    configRowCol(btnClose,1)
except TclError:
    tkMessageBox.showerror("Icon Error", "Unable to load icon")
    
nb = ttk.Notebook(btnStatsFrame, name='nb') # create Notebook in "master"
nb.pack(fill=BOTH) # fill "master" but pad sides

# create each Notebook tab in a Frame
master_foo = ttk.Frame(nb, name='master-foo')
frmInsideTab1=ttk.LabelFrame(master_foo,text="--") 
configGrid(frmInsideTab1,1,2,1,1)
configRowCol(frmInsideTab1,1)

#Add a combox to hold k-tail values (e.g: k=2)
kvalue_label=Label(frmInsideTab1,text="Select value for K",width=15).pack(side=tk.TOP)
#configGrid(kvalue_label,1,1,1,1)
#configRowCol(kvalue_label,1)
box_value = StringVar()
box = ttk.Combobox(frmInsideTab1, textvariable=box_value, 
                                    state='readonly',text='k-tail',width=15,justify=RIGHT)
box.bind("<<ComboboxSelected>>", kValueSelectormethod)
box['values'] = ('1', '2', '3','4','5')
box.current(1)
box.pack(side=tk.TOP)
configRowCol(box,1)

#Add a button inside the tab

btnGenerate=ttk.Button(frmInsideTab1,text="Generate Automata",width=15,command=generateAutomata)
btnGenerate.pack(side=tk.TOP)
nb.add(master_foo, text="Main") # add tab to Notebook

master_bar = ttk.Frame(btnStatsFrame, name='master-bar')

def lbItemClicked(event):
    """
    function to read the listbox selection
    and put the result in an entry widget
    """
    # get selected line index
    index = listBox.curselection()[0]
    # get the line's text
    seltext = listBox.get(index)
    if len(sAlias.get())!=0:
        sAlias.delete(0, END)

    sAlias.insert(END, seltext)
    return index
    
def _update_listbox(self,indx,oldValue,updatedValue):
        listBox.delete(indx,oldValue)
        listBox.insert(indx,updatedValue)

sAlias=ttk.Entry(master_bar,width=10,textvariable=stateAlias)
sAlias.pack(side=tk.TOP)
#Bind return event to the textbox
# pressing the return key will update edited line
sAlias.bind('<Return>', set_list)

scrollBar = Scrollbar(master_bar)
scrollBar.pack(side=RIGHT, fill=Y)
listBox = Listbox(master_bar, selectmode=tk.SINGLE,width=15,height=5)
listBox.pack(side=LEFT, fill=Y,anchor=W)
scrollBar.config(command=listBox.yview)
listBox.config(yscrollcommand=scrollBar.set)
#Bind the listbox to the mouse click event
listBox.bind('<ButtonRelease-1>',lbItemClicked)

nb.add(master_bar, text="State Alias")
    
action=ttk.Button(objFrame,text="Open Log",command=fileOpen,width=15)
action.grid(column=1,row=3)
#configGrid(btnStatsFrame,1,3,1,1)
configRowCol(action,1)

#create an Import button which will trigger import event to lo traces into the textPad
importButton=ttk.Button(objFrame,text="Load Traces",command=importTraces,width=15)
#importButton.grid(column=1,row=4)
configGrid(importButton,1,4,1,1)
configRowCol(importButton,1)

fName=ttk.Entry(objFrame,width=20,textvariable=fileName)
configGrid(fName,0,3,1,1)
configRowCol(fName,1)
    
textPad = ScrolledText(objFrame, width=30,height=3)
configGrid(textPad,0,4,1,1)
configRowCol(textPad,1)

configRowCol(btnGenerate,1)
label = Label(win) #create a label keep a reference to FSM image called from loadFSMImage function

#Add a text area to display log information     
statsPad=ScrolledText(statsTextDisplayFrame,width=150,height=12,wrap=WORD,background='black',foreground='green')
#statsPad.grid(column=0,row=4)
configGrid(statsPad,0,4,1,1)
configRowCol(statsPad,1)

#Add a canvas to the stateDiagramFrame
canvas=Canvas(stateDiagramFrame,bg='#FFFFFF',width=400,height=420)
canvas.pack(side="top", fill="both", expand=True)

#Add a scrollbar for the canvas
setScrollBar(canvas,stateDiagramFrame)
#bind scroll left-to-right scroll events to the canvas
canvas.bind('<4>', lambda event : canvas.xview('scroll', -1, 'units'))
canvas.bind('<5>', lambda event : canvas.xview('scroll', 1, 'units'))
canvas.focus_set()

#Add a status bar label
statusBar=Label(win,text="K-TAIL ALGORITHM : ",bd=1,anchor='w',bg='gray',width=152,justify=LEFT)
statusBar.tkraise()
statusBar.grid(column=0,row=6)

def loadStatsLogToTextBox(k,lst):
    if len(statsPad.get('1.0', END))>0:
        statsPad.delete('1.0', END)
            
    from ktail import kTails
    kt=kTails('K-TAILS')
    kt.do_kTailEquivCheck(k, lst,stateAliasMapList)
    ktfsm=kTailFSMGraph('FSM')
    
    statsPad.insert(END,'Identifying Equivalent k-tails (k=' + str(box.get()) +')\n')
    statsPad.insert(END,'-----------------------------------------------------------------------------------------------------------------------------------\n')
    if len(kt.strEquiv)==0:
        statsPad.insert(END, str('No Equivalent k-tails found with k=' + str(box.get())) +'\n')
        
    for streq in kt.strEquiv:
        statsPad.insert(END, str(streq)) #+ '\n')
    
    statsPad.insert(END,'-----------------------------------------------------------------------------------------------------------------------------------\n')
    statsPad.insert(END, 'Initial States + Corresponding labels : ' +str(kt.state)+ '\n')
    statsPad.insert(END, 'Equivalent States: ' +str(kt.nodelist)+ '\n')
    statsPad.insert(END, 'Merged States :' + str(kt.mergedlist)+ '\n')
    statsPad.insert(END,'-----------------------------------------------------------------------------------------------------------------------------------\n')

    statsPad.insert(END,'Mapping : ' +str(ktfsm.mapping) +'\n')
    statsPad.insert(END,'State Map : '+str(ktfsm.stateMap) +'\n')
    statsPad.insert(END,'-----------------------------------------------------------------------------------------------------------------------------------\n')
    statsPad.insert(END,'Finalised States: '+ str(kTailFSMGraph.getUniqueStates)+'\n')
    statsPad.insert(END,'State-Label: '+ str(kTailFSMGraph.transDict)+'\n')
    statsPad.insert(END,'State Transitions:-----------------------------------------------------------------------------------------------------------------\n')
    for nx,kvx in ktfsm.stateMap.items():
            for c in kvx:
                statsPad.insert(END,str(nx) + '-->'+str(c) + '[label='+kvx[c] +']\n')

    statsPad.insert(END,'***********************************************************************************************************************************\n')
    statsPad.configure(state='disabled')
    
win.mainloop()

    
    
