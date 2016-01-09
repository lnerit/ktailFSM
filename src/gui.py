#!/usr/bin/python
import sys
import os.path
from Tkconstants import END, WORD, FALSE, HORIZONTAL, BOTTOM, X, VERTICAL,\
    RIGHT, Y, BOTH, LEFT, W,SINGLE
from ktail import kTailFSMGraph
import logging
from gtk import TRUE
import tkFont
import re
from fsm import get_graph, FiniteStateMachine, State
from sphinx.ext.graphviz import GraphvizError

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import Tkinter as tk
import ttk
from tkFileDialog import askopenfilename
from ScrolledText import *
from Tkinter import  Canvas, PhotoImage, StringVar, Label, Scrollbar,\
Listbox, Checkbutton, IntVar, TclError, Menu,Toplevel
import tkMessageBox

win = tk.Tk() 
win.title("K-TAIL FINITE STATE AUTOMATA")
win.resizable(width=TRUE, height=TRUE)
width=win.winfo_screenwidth()
height=win.winfo_screenheight()
win.geometry("%dx%d" % (width,height))

#Declare public variables
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
            tracePad.delete('1.0', END) #clear the textbox before loading traces
            with open(fName.get(), 'r') as my_file:
                for line in my_file:
                    #contents.append(line.rstrip().split(','))
                    line=line.strip()
                    contents.append(line)
                
            for row in contents:
                tracePad.insert(0.0, row)   
        except IOError:
            if len(fName.get())==0 or len(fName.get())==1:
                tkMessageBox.showinfo("File Error","No trace log file specified.Please selected a log file")
            else:
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
    if len(tracePad.get('1.0',END))==0 or len(tracePad.get('1.0',END))==1:
        tkMessageBox.showinfo("Empty trace","The trace is empty.Please select a trace log.")
        return
    try:
        text_FromTextBox(tracePad.get('1.0', END).split(','))
        statsPad.configure(state='normal')
        loadEquivalentState=loadStatsLogToTextBox(int(box.get()),columns)

        #load image to canvas
        loadFSMImage()
        #print 'statemap called from GUI'+str(kTailFSMGraph.stateMap)
       
        #Check if the checkbox is checked or not
        if int(var1.get())==0:
            loadStateAliasToListBox(kTailFSMGraph.getUniqueStates, listBox)
                
        #We iterate throug the stateamp dictionary replace each state keys with the alias names
        print("--- %s seconds ---" % (time.time() - start_time))
        #for k,v in stateMapCopy.items():
        #    print k,v   
        aliasDict={}
        for s in kTailFSMGraph.getUniqueStates:
            aliasDict[s]={}
        print aliasDict
            
    except "Error":
        tkMessageBox.showerror("Error", "An error has occured!")
        pass

        
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
    
def loadFSMImage():
    try:
        img = PhotoImage(file="../graph/ktail.png")
        label.image = img # keep a reference!
        imgWidth1 = canvas.winfo_width()
        imgHeight1 =canvas.winfo_height()
        x = (imgWidth1)/2.0
        y = (imgHeight1)/2.0
        canvas.create_image(x, y, anchor=tk.CENTER,image=img,tags="bg_img")
    except TclError:
        #If image file is missing, we generate a new image file
        if img==None:
            generateNewImage
        else:
            tkMessageBox.ERROR
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

def resize(self, event):
    self.font = tkFont(size = stateDiagramFrame.winfo_height())

def setScrollBar(canvas,frame):
    hbar=Scrollbar(frame,orient=HORIZONTAL)
    hbar.pack(side=BOTTOM,fill=X)
    hbar.config(command=canvas.xview)
    vbar=Scrollbar(frame,orient=VERTICAL)
    vbar.pack(side=RIGHT,fill=Y)
    vbar.config(command=canvas.yview)
    canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    canvas.pack(side=LEFT,expand=True,fill=BOTH)
    

#Add canvas frame for canvas area to draw image
#stateDiagramFrame=ttk.Frame(win,text='Finite State Automata',width=400,height=400)
#stateDiagramFrame=ttk.Frame(win,width=400,height=500)

stateDiagramFrame=ttk.Frame(win)
stateDiagramFrame.pack(fill = BOTH)

#Build LabelFrame for the objects on the GUI
objFrame=ttk.LabelFrame(win,text='Trace Input')
configRowCol(objFrame,1)
objFrame.pack(fill=BOTH)

statsFrame=ttk.LabelFrame(win,text='K-Tails Log Information...',width=50,height=200)
configRowCol(statsFrame,1)
statsFrame.pack(fill=BOTH,anchor='s')
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
    
nb = ttk.Notebook(btnStatsFrame, name='nb') # create Notebook in "btnStatsFrame"
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
configRowCol(action,1)


fName=ttk.Entry(objFrame,width=20,textvariable=fileName)
configGrid(fName,0,3,1,1)
configRowCol(fName,1)

#create an Import button which will trigger import event to lo traces into the textPad
try:
        importButton=ttk.Button(objFrame,text="Load Traces",command=importTraces,width=15)
        #importButton.grid(column=1,row=4)
        configGrid(importButton,1,4,1,1)
        configRowCol(importButton,1)
except "Empty Log":
    pass
            
tracePad = ScrolledText(objFrame, width=30,height=3)
configGrid(tracePad,0,4,1,1)
configRowCol(tracePad,1)

configRowCol(btnGenerate,1)
label = Label(win) #create a label keep a reference to FSM image called from loadFSMImage function

#Add a text area to display log information     
statsPad=ScrolledText(statsTextDisplayFrame,width=150,height=12,wrap=WORD,background='black',foreground='green')
configGrid(statsPad,0,4,1,1)
configRowCol(statsPad,1)

#Add a canvas to the stateDiagramFrame
canvas=Canvas(stateDiagramFrame,bg='#FFFFFF',height=420)
canvas.pack(side="top", fill="both", expand=True)

#Add a scrollbar for the canvas
setScrollBar(canvas,stateDiagramFrame)
#bind scroll left-to-right scroll events to the canvas
canvas.bind('<4>', lambda event : canvas.xview('scroll', -1, 'units'))
canvas.bind('<5>', lambda event : canvas.xview('scroll', 1, 'units'))
canvas.focus_set()

# create a pulldown menu, and add it to the menu bar
menubar = Menu(win)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open Log", command=fileOpen)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=win.quit)
menubar.add_cascade(label="File", menu=filemenu)

def callChildWindow():

    if TraceLoaded(tracePad)==False:
        tkMessageBox.showerror("No trace Log", "Please load traces first.")
        return
    else:
        from ktail import kTails
        kt=kTails('K-TAILS')
        kt.FiniteAutomata(columns)
        transitionSelection(kt.manualProcessingLog)
        
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Set Manual", command=callChildWindow)
menubar.add_cascade(label="Manual Setting", menu=editmenu)
# display the menu
win.config(menu=menubar)

#Add a status bar label
#statusBar=Label(win,text="K-TAIL ALGORITHM : ",bd=1,anchor='w',bg='gray',width=152,justify=LEFT)
#statusBar.tkraise()
#statusBar.grid(column=0,row=6)

def loadStatsLogToTextBox(k,lst):
    if len(statsPad.get('1.0', END))>0:
        statsPad.delete('1.0', END)
    try:  
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
        statsPad.insert(END, 'Initial States: ' +str(kt.state)+ '\n')
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
    except "Error":
        tkMessageBox.ERROR



#This segment of code generates a toplevel child window
#'============================================================='
#Global variables
manualMappingList=[]
transitionDict={}
stateList=[]
stateMap1={}
var=IntVar()

def TraceLoaded(ScrolledText):
    if  len(ScrolledText.get('1.0',END))==0 or len(ScrolledText.get('1.0',END))==1:
        return False
    else:
        return True
def get_num(x):
    return (''.join(ele for ele in x if ele.isdigit()))
        
def get_apha(x):
    return str(''.join(re.findall("[a-zA-Z]+", x)))
            
def transitionSelection(tracelog,*args):
    # start of child window GUI code
    root = Toplevel()
    root.title("Manual Transition selection")
    root.resizable(width=FALSE, height=FALSE)
    
    # frame
    mainFrame = ttk.Frame(root, width="364", padding="4 4 8 8")
    mainFrame.grid(column=0, row=0)
    
    labelSource=ttk.Label(mainFrame,text="Source", justify=LEFT)
    labelSource.grid(column=0, row=0, sticky="e")
        
    srcState = ttk.Combobox(mainFrame,width=10)
    srcState.delete(0, END)
    srcState['values'] = ([k for k in tracelog])
    srcState.grid(column=1, row=0, sticky="e")        
    srcState.state(['readonly'])
       
    # Destination label
    labelDestination=ttk.Label(mainFrame,text="Destination",justify=LEFT)
    labelDestination.grid(column=0, row=1, sticky="e")
       
    # destination combobox
    destState = ttk.Combobox(mainFrame,width=10)
    destState.delete(0, END)
    destState['values'] = ([get_num(k) for k in tracelog])
    destState.grid(column=1, row=1, sticky="e")
    destState.state(['readonly'])
                  
    listFrame=ttk.LabelFrame(root)
    listFrame.grid(column=0,row=2,sticky="we")
    scrollBar = Scrollbar(listFrame)
    scrollBar.pack(side=RIGHT, fill=Y)
    listBoxTop = Listbox(listFrame, selectmode=SINGLE,width=20,height=10)
    listBoxTop.pack(fill=BOTH)
    scrollBar.config(command=listBoxTop.yview)
    listBoxTop.config(yscrollcommand=scrollBar.set)
                
    def addItemsToList():
        st=get_apha(srcState.get())
        #if int(self.get_num(self.srcState.get()))==0:#Indicate the source state with a *
        #    self.set_list(self.listBox,'*'+str(self.get_num(self.srcState.get())) +'-->'+ str(self.destState.get()) + '['+st+']')
        #    manualMappingList.append('*'+str(self.get_num(self.srcState.get())) +'-->'+ str(self.destState.get()) + '['+st+']')
        #else:
        set_listTop(listBoxTop,str(get_num(srcState.get())) +'-->'+ str(destState.get()) + '[label='+st+']')
        manualMappingList.append(str(get_num(srcState.get())) +'-->'+ str(destState.get()))
        transitionDict[get_num(srcState.get())]=st
            
    def OnDouble():
        try:
            if len(listBoxTop.get(0, END))==0 or listBoxTop.curselection() is None:
                tkMessageBox.showerror("Empty List", "The mapping list is empty")
                return
            else:
                selection=listBoxTop.curselection()
                value = listBoxTop.get(selection[0])
                #print "selection:", selection, ": '%s'" % value
                        
                ch=''
                for c in value:
                    if c=='[': #Strip out characters after the symbol [
                        break
                    else:
                        ch +=c
            #when we remove an entry from the listbox, we also update the manual mapping list
            manualMappingList.remove(ch)
            listBoxTop.delete(selection) #remove the selected entry from listbox
        except (IndexError,AttributeError,ValueError):
            tkMessageBox.showerror("Error", "Please select an entry if exists or try again")
        
    def removeMapFromList():
        """
        function to read the listbox selection
        and put the result in an entry widget
        """
        try:
            # get selected line index
            index = listBoxTop.curselection()[0]
            # get the line's text
            manualMappingList.remove(str(listBoxTop.curselection()))
            listBoxTop.delete(index)
        except (ValueError,IndexError):
            pass
            
    def generateFSMGraph():
        
        for e in transitionDict:
            print transitionDict[e]
            stateMap1[int(e)]={}
            for m in manualMappingList:
                st=[int(s) for s in m.split('-->') if s.isdigit()] #extract digits in a mapping entry
                if str(e)==str(st[0]) and str(e)==str(st[1]):    
                    stateMap1[int(e)][int(st[0])]=transitionDict[e]
                elif str(e)!=str(st[1]) and str(e)==str(st[0]):
                    stateMap1[int(e)][int(st[1])]=transitionDict[e]
        #callback functions    
        drawStateTransitionGraph()
        loadFSMImage()

    def closeWindowTop():
        root.destroy()
    
    #Add a button inside the tab
    btnAdd=ttk.Button(mainFrame,text="Add",width=10,command=addItemsToList)
    btnAdd.grid(column=2,row=0)                
    btnRemove=ttk.Button(mainFrame,text="Remove",width=10,command=OnDouble)
    btnRemove.grid(column=2,row=1)
    
    #Add frame to hold buttons
    btnFrame=ttk.LabelFrame(root)
    btnFrame.grid(column=0,row=3,sticky="we")
    btnCancel=ttk.Button(btnFrame,text="Cancel",width=13,command=closeWindowTop)
    btnCancel.pack(side=RIGHT,fill=X)
    btnOk=ttk.Button(btnFrame,text="Generate FSM",width=13,command=generateFSMGraph)
    btnOk.pack(side=RIGHT, fill=X)
  
    def set_listTop(Listbox,sMap):
            try:
                index=Listbox.curselection()[0]
                #Check if there is an existing entry in the listbox
            except IndexError:
                index=END
            for i,listbox_entry in enumerate(Listbox.get(0, END)):
                if listbox_entry == sMap:
                    tkMessageBox.showinfo("Entry", "There is already an entry for this transition.")
                    return
    
            Listbox.insert(index, sMap)
            
                
    def drawStateTransitionGraph():
        #Here we appy the state transitions to create a finite state machine
        ktail = FiniteStateMachine('K-TAIL')
        for nx,kvx in stateMap1.items():
                for c in kvx:
                    State(nx).update({kvx[c]:State(c)})
                    print 'State Transition: ' +str(nx) + '-->'+str(c) + '[label='+kvx[c] +']'
                #Define initial state    
                if nx==0:
                        nx=State(0, initial=True)
        #Create a state machine
        print '------------------------------------------------------------------------------------'
        #Check if there is existing graph data 
        try:
            graph=get_graph(ktail)
            if graph!=None:
                graph.draw('../graph/ktail.png', prog='dot')
                print graph
            else:
                pass
        except GraphvizError:
            tkMessageBox.ERROR
            
    # padding for widgets
    for child in mainFrame.winfo_children(): child.grid_configure(padx=4, pady=4)
                                    
    root.mainloop()
               
win.mainloop()

