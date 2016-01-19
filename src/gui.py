#!/usr/bin/python
import sys
import os.path
from Tkconstants import END, WORD, FALSE, HORIZONTAL, BOTTOM, X, VERTICAL,\
    RIGHT, Y, BOTH, LEFT,SINGLE
from ktail import kTailFSMGraph
import logging
from gtk import TRUE
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
multitrace={}
sampleStatus=''
#Check button to validate trace against the sample trace input automata
sInputCheck=IntVar()

def __init__(self,param):
    self.log=logging.getLogger('gui.py')
    
def fileOpen():
    try:
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
            #contents=[]
            tracePad.delete('1.0', END) #clear the textbox before loading traces
            print file(fName.get(), "r").read().replace("\n", ", ")
            #with open(fName.get(), 'r') as my_file:
            #    txt=''
            #    for line in my_file:
                    #contents.append(line.rstrip().split(','))
            #        line=line.strip().replace('\n',',')
            #        contents.append(line)
                    #print str(line+'\n').replace('\n', ',')
            
            row=file(fName.get(), "r").read().replace("\n", ", ")
            tracePad.insert(0.0, row)
            #tracePad.insert(0,0, )   
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
    #try:
    text_FromTextBox(tracePad.get('1.0', END).split(','))
    statsPad.configure(state='normal')
    
    loadStatsLogToTextBox(int(box.get()),columns,1)

    loadFSMImage()

    print("--- %s seconds ---" % (time.time() - start_time))
        
            
    #except "Error":
    #    tkMessageBox.showerror("Error", "An error has occured!")
        #pass

def kValueSelectormethod (self):
        print("method is called")
        
#If there is no image file ktail.png, then create a blank image file to draw the transition graph       

def loadFSMImage():
    
    try:
        img = PhotoImage(file="../graph/ktail.png")
        label.image = img # keep a reference!
        imgWidth1 = canvas.winfo_width()
        imgHeight1 =canvas.winfo_height()
        x = (imgWidth1)/2.0
        y = (imgHeight1)/2.0
        canvas.delete(img) #reset canvas
        canvas.create_image(x, y, anchor=tk.CENTER,image=img,tags="bg_img")
       
    except TclError:
        #If image file is missing, we generate a new image file
        tkMessageBox.ERROR
        return
    

def closeWindow():
    win.destroy()
            
def configRowCol(objectx,weight):
    objectx.rowconfigure(0,weight=weight)
    objectx.columnconfigure(0,weight=weight)
    return objectx

def configGrid(objectx,col,row,colspan,rowspan):
    objectx.grid(column=col,row=row,rowspan=rowspan, columnspan=colspan, sticky=(tk.N, tk.S, tk.W, tk.E))
    return objectx

#def resize(self, event):
#    self.font = tkFont(size = stateDiagramFrame.winfo_height())

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

stateDiagramFramePreview=ttk.Frame(win)
stateDiagramFramePreview.pack(side=BOTTOM,fill='x')

#Build LabelFrame for the objects on the GUI
objFrame=ttk.LabelFrame(win,text='Trace Input')
configRowCol(objFrame,1)
objFrame.pack(fill=BOTH,side=tk.TOP)

filenamePadFrame=ttk.LabelFrame(objFrame,text="File name")
filenamePadFrame.grid(column=0,row=2,sticky='ewns')
configRowCol(filenamePadFrame,1)


tracePadFrame=ttk.LabelFrame(objFrame,text="Sample Trace")
tracePadFrame.grid(column=0,row=3,sticky='ewns')
configRowCol(tracePadFrame,1)

statsFrame=ttk.LabelFrame(win,text='K-Tails Log Information...',width=50,height=200)
configRowCol(statsFrame,1)
statsFrame.pack(fill=BOTH,anchor='s')

#Add a frame for the stats display text area
statsTextDisplayFrame=ttk.LabelFrame(statsFrame,text='DisplayLog...',width=50,height=100)
#statsTextDisplayFrame.grid(column=0,row=2,rowspan=1, columnspan=1, sticky=(tk.N, tk.S, tk.W, tk.E))
configGrid(statsTextDisplayFrame,0,2,1,1)
configRowCol(statsTextDisplayFrame,1)

def displaysampleAutomata():
    global samplaCanvas
    global frameSampleDisplay
    if sInputCheck.get()==1:
        import resizeimage
        frameSampleDisplay=ttk.LabelFrame(statsFrame,width=300,height=200)
        configGrid(frameSampleDisplay,1,2,1,1)

        samplaCanvas=Canvas(frameSampleDisplay,bg='#FFFFFF',height=200,width=300)
        samplaCanvas.pack(side=LEFT,fill=BOTH)
        filename='../graph/sample.png'
        resizeimage.resizeImage(filename,0.5)
        img = PhotoImage(file="../graph/sample0.5.png")
       
        label1.image = img # keep a reference!
        
        samplaCanvas.delete(img) #reset canvas
        samplaCanvas.create_image(0, 80, anchor='nw',image=img,tags="bg_img")
        hbar=Scrollbar(frameSampleDisplay,orient=HORIZONTAL)
        hbar.pack(side=BOTTOM,fill=X)
        hbar.config(command=samplaCanvas.xview)
        vbar=Scrollbar(frameSampleDisplay,orient=VERTICAL)
        vbar.pack(side=RIGHT,fill=Y)
        vbar.config(command=samplaCanvas.yview)
        canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
       
    else:
        frameSampleDisplay.destroy()
        
#btnClosex=ttk.Button(sampleFrame,text="Close window",command=closeWindow,width=15)
#btnClosex.pack(side=tk.BOTTOM,anchor=tk.N,fill=BOTH)

btnStatsFrame=ttk.LabelFrame(statsFrame,text='---') 
configGrid(btnStatsFrame,2,2,1,1)
configRowCol(btnStatsFrame,1)

nb = ttk.Notebook(btnStatsFrame, name='nb') # create Notebook in "btnStatsFrame"
nb.pack(fill=BOTH) # fill "master" but pad sides

# create each Notebook tab in a Frame
master_foo = ttk.Frame(nb, name='master-foo')
frmInsideTab1=ttk.LabelFrame(master_foo,text="--") 
configGrid(frmInsideTab1,1,2,1,1)
configRowCol(frmInsideTab1,1)

#Add a combox to hold k-tail values (e.g: k=2)
kvalue_label=Label(frmInsideTab1,text="Select value for K",width=15).pack(side=tk.TOP)
box_value = StringVar()
box = ttk.Combobox(frmInsideTab1, textvariable=box_value, 
                                    state='readonly',text='k-tail',width=15,justify=RIGHT)
#box.bind("<<ComboboxSelected>>", kValueSelectormethod)
box['values'] = ('1', '2', '3','4','5')
box.current(1)
box.pack(side=tk.TOP)
configRowCol(box,1)

#Generic function for combining functions
def combine_funcs(*funcs):
    def combine_func(*args,**kwargs):
        for f in funcs:
            f(*args,**kwargs)
    return combine_func

validateAgainstsample=IntVar()
def get_sInputCheck():
    return validateAgainstsample.get()

#Add a button inside the tab
btnGenerate=ttk.Button(frmInsideTab1,text="Generate Automata",width=15,command=generateAutomata)
btnGenerate.pack(side=tk.TOP)
sampleAutomataChk=Checkbutton(frmInsideTab1,text="Validate against sample",variable=validateAgainstsample,command=get_sInputCheck)
sampleAutomataChk.pack(side=tk.TOP)



acceptrejectStatusvalue=Label(frmInsideTab1,text=sampleStatus,width=10,bg='blue')
acceptrejectStatusvalue.pack(anchor='w',side=tk.TOP,fill=X)
#acceptrejectStatuslbl=Label(frmInsideTab1,text="Status:",width=4)
#acceptrejectStatuslbl.pack(anchor='w',side=tk.TOP)
def displayFromBrowser():
    if len(canvas.find_all())==0:
        tkMessageBox.showinfo("FSM", 'Nothing to show.Please generate an FSM first')
        return
    
    import webbrowser
    webbrowser.open('../graph/ktail.png') 

externalDisplay=ttk.Button(frmInsideTab1,text="Print",command=closeWindow,width=3)
externalDisplay.pack(anchor='w',fill=X)
externalDisplay1=ttk.Button(frmInsideTab1,text="Browser View",command=displayFromBrowser,width=3)
externalDisplay1.pack(anchor='w',fill=X)

try:
    photo1 = tk.PhotoImage(file="../icon/dialog_cancel.png")
    btnClose=ttk.Button(frmInsideTab1,text="Close window",image=photo1,command=closeWindow,width=10)
    btnClose.pack(side=BOTTOM,anchor='w',fill=X)
    #configRowCol(btnClose,1)
except TclError:
    tkMessageBox.showerror("Icon Error", "Unable to load icon")
    
nb.add(master_foo, text="Trace Input") # add tab to Notebook

master_bar = ttk.Frame(btnStatsFrame, name='master-bar')
sampleFrame=ttk.LabelFrame(master_bar,text='Sample State')
configGrid(sampleFrame,1,2,1,1)
configRowCol(sampleFrame,1)
innersampleFrame=ttk.LabelFrame(sampleFrame)
innersampleFrame.grid(column=0,row=0,sticky='ewns',)
#configGrid(innersampleFrame,0,0,1,1)
configRowCol(innersampleFrame,1)

labelSource=ttk.Label(innersampleFrame,text="Start Start", justify=LEFT)
labelSource.grid(column=0, row=0, sticky="nw")
#labelSource.pack(side=tk.TOP,anchor='w')   
srcStateTextVariable=StringVar()
srcState = ttk.Combobox(innersampleFrame,width=10,textvariable=srcStateTextVariable)
srcState.delete(0, END)
#srcState['values'] = ([k for k in columns])
srcState.grid(column=1, row=0, sticky="ne")
#srcState.pack(side=tk.TOP, anchor='e')#(column=1, row=0, sticky="e")          
srcState.state(['readonly'])
#srcState.bind("<<ComboboxSelected>>", kValueSelectormethod)

    # Destination label
labelDestination=ttk.Label(innersampleFrame,text="Accept States",justify=LEFT)
#labelDestination.pack(side=LEFT,anchor='w')
labelDestination.grid(column=0, row=1, sticky="nw")

def acceptStatesSelected(event):
    if len(acceptStatestEntry.get())==0:
        acceptStatestEntry.insert(END,str(destStateTextVariable.get()))
    else:
        acceptStatestEntry.insert(END,','+ str(destStateTextVariable.get()))
    # destination combobox
destStateTextVariable=StringVar()
destState = ttk.Combobox(innersampleFrame,width=4,textvariable=destStateTextVariable)
destState.delete(0, END)
destState.grid(column=1 , row=1, sticky="nw")
#destState.pack(tk.TOP)
destState.state(['readonly'])
destState.bind("<<ComboboxSelected>>", acceptStatesSelected)


acceptStatesTextVariable=StringVar()
acceptStatestEntry = ttk.Entry(innersampleFrame,width=4,textvariable=acceptStatesTextVariable)
acceptStatestEntry.grid(column=1 , row=1, sticky="e")

listFrame=ttk.LabelFrame(sampleFrame)
listFrame.grid(column=0,row=1,sticky="ewns")
scrollBar = Scrollbar(listFrame)
scrollBar.pack(side=RIGHT, fill=Y)
listBoxTop = Listbox(listFrame, selectmode=SINGLE,width=10,height=5)
listBoxTop.pack(fill=BOTH)
scrollBar.config(command=listBoxTop.yview)
listBoxTop.config(yscrollcommand=scrollBar.set)

sampleInputOption=Checkbutton(listFrame,text='Display Automata',variable=sInputCheck,command=displaysampleAutomata)
sampleInputOption.pack(side=tk.LEFT, fill='x',anchor='w')
#sampleInputOption.bind('<>',displaysampleAutomata)

nb.add(master_bar, text="Sample Input")

def generateSampleAutomata():
    try:
        import time
        start_time=time.time()
        if len(samplePad.get())==0 or len(samplePad.get())==1:
            tkMessageBox.showinfo("Empty trace","Sample trace is empty.Please select a trace log.")
            return
        #try:
        text_FromTextBox(samplePad.get().split(','))
        statsPad.configure(state='normal')
            
        from ktail import kTails
        import ktail
        kt=kTails('K-TAILS')
        kt.do_kTailEquivCheck(int(box.get()),columns,0)
        
        srcState.delete(0,END)
        srcState['values'] = ([k for k in ktail.getUniqueStatesSample])
        if len( srcState['values'])>0:
            srcState.current(0)
        else:
            pass
            
        acceptStatestEntry.delete(0,END)
        destState.delete(0,END)
        destState['values'] = ([k for k in ktail.getUniqueStatesSample])
        if len( destState['values'])>0:
            print destState['values'][-1]
            destState.current(destState['values'][-1])
            acceptStatestEntry.insert(END,str(destStateTextVariable.get()))
            #acceptStatestEntry.insert(END, destState.current(destState['values'][-1]))
            
        else:
            pass
        
        sampleTransition=ktail.sampleTransitionmapping
        listBoxTop.delete(0,END)
        for k,v in sampleTransition.items():
            p,q=k
            listBoxTop.insert(END,str(p)+'-->'+str(v)+'[label='+q+']')
            
        print("--- %s seconds ---" % (time.time() - start_time))
        
    except (TypeError,TclError,ValueError):
        pass
    
fName=ttk.Entry(filenamePadFrame,width=30,textvariable=fileName)
fName.grid(column=0,row=2,sticky='ewns')
configRowCol(fName,1)

action=ttk.Button(filenamePadFrame,text="Open Log",command=fileOpen,width=12)
action.grid(column=1,row=2)
configRowCol(action,1)

#create an Import button which will trigger import event to lo traces into the textPad
frameMultitrace=ttk.Frame(tracePadFrame)
frameMultitrace.grid(column=1,row=1)
multitraceOption=IntVar()

samplePad = ttk.Entry(tracePadFrame, width=20)
configGrid(samplePad,0,0,1,1)
#configRowCol(samplePad,1)

try:
    importButton=ttk.Button(frameMultitrace,text="Load Traces",command=importTraces,width=10)
    importButton.grid(column=1,row=5,sticky='w')
    configRowCol(importButton,1)
except "Empty Log":
    pass

sampleInputGenerateButton = ttk.Button(tracePadFrame,text='Process Sample',width=15,command=generateSampleAutomata)
configGrid(sampleInputGenerateButton,1,0,1,1)

tracePad = ScrolledText(tracePadFrame, width=10,height=3)
configGrid(tracePad,0,1,1,1)
configRowCol(tracePad,1)

# create a pulldown menu, and add it to the menu bar
menubar = Menu(win)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open Log", command=fileOpen)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=win.quit)
menubar.add_cascade(label="File", menu=filemenu)

configRowCol(btnGenerate,1)
label = Label(win) #create a label keep a reference to FSM image called from loadFSMImage function
label1 = Label(win) #create a label to keep  a reference to sample FSM image
#Add a text area to display log information
  
statsPad=ScrolledText(statsTextDisplayFrame,width=150,height=15,wrap=WORD)
configGrid(statsPad,0,4,1,1)
configRowCol(statsPad,1)

#Add frame for the transition diagram
ht=win.winfo_screenheight()-menubar.winfo_height()-objFrame.winfo_height()-statsFrame.winfo_height()
stateDiagramFrame=ttk.LabelFrame(win,text="Display")
stateDiagramFrame.pack(fill=BOTH,anchor='s')

#Add a canvas to the stateDiagramFrame

canvas1Frame=ttk.LabelFrame(stateDiagramFrame,text="Canvas1")
canvas1Frame.pack(side="top",fill=BOTH)

canvas=Canvas(canvas1Frame,bg='#FFFFFF',height=ht)
#canvas.scalex=1.0
canvas.pack(side="top", fill=BOTH, expand=True)

#Add a scrollbar for the canvas
setScrollBar(canvas,canvas1Frame)
#bind scroll left-to-right scroll events to the canvas
canvas.bind('<4>', lambda event : canvas.xview('scroll', -1, 'units'))
canvas.bind('<5>', lambda event : canvas.xview('scroll', 1, 'units'))
canvas.focus_set()

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

def loadStatsLogToTextBox(k,lst,flag):
    if len(statsPad.get('1.0', END))>0:
        statsPad.delete('1.0', END)
    try:  
        from ktail import kTails
        import ktail
        kt=kTails('K-TAILS')
        kt.do_kTailEquivCheck(k, lst,flag)
        ktfsm=kTailFSMGraph('FSM')
        
        statsPad.insert(END,'Identifying Equivalent k-tails (k=' + str(box.get()) +')\n')
        statsPad.insert(END,'-----------------------------------------------------------------------------------------------------------------------------------\n')
        if len(kt.strEquiv)==0:
            statsPad.insert(END, str('No Equivalent k-tails found with k=' + str(box.get())) +'\n')
        if multitraceOption.get()==1:
            if len(kt.strEquiv2)==0:
                statsPad.insert(END, str('No Equivalent k-tails found with k=' + str(box.get())) +'for Trace 2\n')
                
        for streq in kt.strEquiv:
            statsPad.insert(END, str(streq)) #+ '\n')
         
        statsPad.insert(END,'-----------------------------------------------------------------------------------------------------------------------------------\n')
        statsPad.insert(END, 'Initial States in Trace 1: ' +str(kt.state)+ '\n') 
        statsPad.insert(END, 'Equivalent States in Trace 1: ' +str(kt.nodelist)+ '\n')
        statsPad.insert(END, 'Merged States in Trace 1:' + str(kt.mergedlist)+ '\n')
        statsPad.insert(END,'Mapping in Trace 1: ' +str(kt.mapping) +'\n')
        statsPad.insert(END,'State Map Dictionary in Trace 1: '+str(ktfsm.stateMap) +'\n')
        statsPad.insert(END,'Finalised States in Trace 1: '+ str(kt.getUniqueStates1)+'\n')
        statsPad.insert(END,'++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
        
        #statsPad.insert(END,'Mapping in Trace 1: ' +str(kt.mapping) +'\n')
        #statsPad.insert(END,'State Map in Trace 1: '+str(ktfsm.stateMap) +'\n')
        #statsPad.insert(END,'-----------------------------------------------------------------------------------------------------------------------------------\n')
        #statsPad.insert(END,'Finalised States: '+ str(kTailFSMGraph.getUniqueStates)+'\n')
        statsPad.insert(END,'State-Label in Trace 1: '+ str(kTailFSMGraph.transDict)+'\n')
        statsPad.insert(END,'State Transitions:-----------------------------------------------------------------------------------------------------------------\n')
        for nx,kvx in ktfsm.stateMap.items():
                for c in kvx:
                    statsPad.insert(END,str(nx) + '-->'+str(c) + '[label='+kvx[c] +']\n')
    
        statsPad.insert(END,'***********************************************************************************************************************************\n')
        
        if validateAgainstsample.get()==1:
            statsPad.insert(END,'Processing Automata for Sample Input\n')
            from dfa import DFA
            if srcStateTextVariable is not None:
                #DFA.start_state=int(srcStateTextVariable.get())
                start_state=int(srcStateTextVariable.get())
                print 'Initial State: ' + str(srcStateTextVariable.get())
                statsPad.insert(END,'Initial State: '+ str(srcStateTextVariable.get())+'\n')
            else:
                tkMessageBox.showerror("Initial State","Not Intial state defined. Please check the stting panel")
                #return
            accept_states=set()
            if len(acceptStatestEntry.get())>0:
                #DFA.accept_states={int(destStateTextVariable.get())}
                
                for item in str(acceptStatestEntry.get()).split(','):
                    accept_states.add(int(item))
                #accept_states={acceptStatestEntry.get()}
                print 'Accepting States: ' + str(acceptStatestEntry.get())
                statsPad.insert(END,'Accepting State: ' + str(acceptStatestEntry.get())+'\n')
            else:
                tkMessageBox.showerror("Accepting state","No accepting states defined. Please check the setting panel")
                
            getUniqueStatesSample=ktail.getUniqueStatesSample
            print 'Sample States: ' + str(getUniqueStatesSample)
            statsPad.insert(END,'Sample States: ' + str(getUniqueStatesSample)+'\n')
            sampleTransitionmapping=ktail.sampleTransitionmapping
            
            print 'Sample Transitions: ' + str(sampleTransitionmapping)
            statsPad.insert(END,'Sample Transitions:\n')
            for k,v  in sampleTransitionmapping.items():
                p,q=k
                statsPad.insert(END,str(p)+'--->'+str(v)+'[label='+q+']\n')
            
            alphabet=ktail.alphabet
            print 'Alphabet from sample: ' + str( alphabet)
            statsPad.insert(END,'Alphabet from sample: ' + str( alphabet)+'\n')
            d=DFA(getUniqueStatesSample, alphabet,sampleTransitionmapping,start_state,accept_states,1);
            alphabetfromtrace=kTailFSMGraph.alphabetfromtrace
            print 'yyyyyyy ' + str(sampleTransitionmapping)
            testalphabet=[]
            for k,v in alphabetfromtrace.items():
                p,q=k
                testalphabet.append(q)
            print 'Input Alphabet from Trace ' + str(testalphabet)
            statsPad.insert(END,'Input Alphabet from Trace ' + str(testalphabet)+'\n')
            
            sampleStatus=''
            if d.run_with_input_list(testalphabet):
                sampleStatus=' ACCEPT'
                acceptrejectStatusvalue['text']=sampleStatus
                acceptrejectStatusvalue['bg']='green'
                print 'Status:'+sampleStatus
            else:
                sampleStatus='REJECT'
                acceptrejectStatusvalue['text']=sampleStatus
                acceptrejectStatusvalue['bg']='red'
                print 'ACCEPT/REJECT Status:'+sampleStatus
            statsPad.insert(END,'++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
            for l in d.loginformation:
                print l
                statsPad.insert(END,l+'\n')
                
            d.loginformation=[]
            print 'emty' + str(d.loginformation)
            statsPad.insert(END,'Status: ' + sampleStatus+'\n')
            
        statsPad.insert(END,'++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
         
        statsPad.configure(state='disabled')
    except (ValueError):
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
        
        if len(srcState.get())==0:
            tkMessageBox.showerror("No Source Entry","Please select a source state first")
            root.focus()
            return
        else:
            
            st=get_apha(srcState.get())
            set_listTop(listBoxTop,str(get_num(srcState.get())) +'-->'+ str(destState.get()) + '[label='+st+']')
            manualMappingList.append(str(get_num(srcState.get())) +'-->'+ str(destState.get()))
            transitionDict[get_num(srcState.get())]=st
            
            generateFSMGraph()
        
    def removeMapFromList():
        try:
            if len(listBoxTop.get(0, END))==0 or listBoxTop.curselection() is None:
                tkMessageBox.showerror("Empty List", "The mapping list is empty")
                return
            else:
                selection=listBoxTop.curselection()
                value = listBoxTop.get(selection[0])
                
                        
                ch=''
                for c in value:
                    if c=='[': #Strip out characters after the symbol [
                        break
                    else:
                        ch +=c
            #when we remove an entry from the listbox, we also update the manual mapping list
            manualMappingList.remove(ch)
            listBoxTop.delete(selection) #remove the selected entry from listbox
            generateFSMGraph()
            transitionDict={} #reset the transition dictionary to capture updated entries from the listBox
            
        except (IndexError,AttributeError,ValueError):
            tkMessageBox.showerror("Error", "Please select an entry if exists or try again")
        
    '''    
    def onDouble():
        """
        function to read the listbox selection
        and put the result in an entry widget
        """
        if listBoxTop.curselection()[0] is None:
            tkMessageBox.showerror("No entry","Nothing to remove")
            return
        
        try:
            # get selected line index
            index = listBoxTop.curselection()[0]
            # get the line's text
            manualMappingList.remove(str(listBoxTop.curselection()))
            listBoxTop.delete(index)
        except (ValueError,IndexError):
            pass
    '''        
    def generateFSMGraph():
        if len(listBoxTop.get(0, END))==0:
            tkMessageBox.showerror("No entry","There is no mapping entry.Please add mapping entry first")
            return
        try:
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
            
        except (ValueError,IndexError,GraphvizError,AttributeError):
            pass
        
    def closeWindowTop():
        root.destroy()
    
    #Add a button inside the tab
    btnAdd=ttk.Button(mainFrame,text="Add",width=10,command=addItemsToList)
    btnAdd.grid(column=2,row=0)                
    btnRemove=ttk.Button(mainFrame,text="Remove",width=10,command=removeMapFromList)
    btnRemove.grid(column=2,row=1)
    
    #Add frame to hold buttons
    btnFrame=ttk.LabelFrame(root)
    btnFrame.grid(column=0,row=3,sticky="we")
    btnCancel=ttk.Button(btnFrame,text="Close",width=13,command=closeWindowTop)
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



#Add a button to close the window inside the tab
#closeButtonFrame=Labelframe(win)
#closeButtonFrame.pack(side=LEFT,anchor=tk.S,fill=BOTH)




win.mainloop()

