
'''
Created on 15/12/2015
@author: lenz l nerit
'''
import sys
import os.path
import logging
from sphinx.ext.graphviz import GraphvizError
import tkMessageBox


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from itertools import combinations
from collections import OrderedDict
from fsm import FiniteStateMachine, get_graph, State

#from ktail import ktail 

#tDict=[] #OrderedDict()
#tMap=OrderedDict() #This is an ordered dictionary to store state transition mapping   
tmpDict=OrderedDict()
tmpDict2=OrderedDict()

def group_States(nodelist):
    sets = [set(x) for x in nodelist] 
    stable = False
    while not stable:                        # loop until no further reduction is found
        stable = True
        # iterate over pairs of distinct sets
        for s,t in combinations(sets, 2):
            if s & t:                        # do the sets intersect ?
                s |= t                       # move items from t to s 
                t ^= t                       # empty t
                stable = False
                                                
                # remove empty sets
                sets = list(filter(None, sets)) # added list() for python 3
        #try:
        if len(sets)==0:
            pass
        return sets          

#This function checks for equivalent states based k-tails strings
#for two states p,q. If matched found then returns True and False otherwise
def check_equivalence(p,q):
    if p==q: 
        return True
    else:
        return False
    
def transitionMapping(lst):
        current = None
        nxt = None
        index=0
        mapping=[]
        while (index+1)<len(lst):
                current=lst[index]
                nxt=lst[index+1]
                mapping.append(str(current) +'-->'+ str(nxt))
                index+=1
        return mapping
        
def get_num(x):
    return (''.join(ele for ele in x if ele.isdigit()))

getUniqueStatesSample=set()

samplealphabet=set()
transDictSample={}
sampleTransitionmapping={} 

class kTails():
    '''
    This class implements the k-tails algorithm to compare equivalent states
    and merge them before a minimal fsm is produced
    '''
    #trace=['A','B','C','A','B','C','A','B','C','A','B','C']
    k=3 # set default value to 3  but overwritten with user input
    alphabet=[]
    def __init__(self, params):
        self.log=logging.getLogger('ktail.py')
        pass
        '''
        Constructor
        '''     
    
    def state(self):
        self.state=[]
        return self.state
    
    def nodelist(self):
        self.nodelist=[[]]
        return self.nodelist
    
    def mergedlist(self):
        self.mergedList=[]
        return self.mergedList
    def tmpDict(self):
        return tmpDict
    
    def strEquiv(self):
        self.strEquiv=[]
        return self.strEquiv
    def manualProcessingLog(self):
        self.manualProcessingLog=[]
        return self.manualProcessingLog
    
    def FiniteAutomata(self,seq):
        sequence=list(seq) #A list containing sequences of traces
        kTails.stateFA=[]
        kTails.nodelistFA=[[]]
        kTails.strEquivFA=[]
        
        kTails.manualProcessingLog=[]
        for x in range(0,len(sequence)):
            kTails.stateFA.append(x)
            #print str(x) + '[label='+sequence[x]+']'
            self.manualProcessingLog.append(str(x) + '['+sequence[x]+']')
            
        mergedlistFA=list(kTails.stateFA) 
        
        for i in range(0,len(kTails.stateFA)):
            #tmpDictFA[i]=sequence[i]  
            for ind in kTails.stateFA:
                if check_equivalence(sequence[i:1+i],sequence[ind+1+i:ind+1+1+i]):       
                    kTails.nodelistFA.append(set([i,ind+1+i+1]))
                    if i in mergedlistFA: 
                        mergedlistFA[ind+i+1]=i
                           
    def sampleAutomata(self,seq):
        sequence=list(seq) #A list containing sequences of traces
        kTails.stateSample=[]
        kTails.nodelistSample=[[]]
        kTails.strEquivSample=[]
        
        kTails.sampleProcessingLog=[]
        for x in range(0,len(sequence)):
            kTails.stateSample.append(x)
            #print str(x) + '[label='+sequence[x]+']'
            self.sampleProcessingLog.append(x) #+ '['+sequence[x]+']')
            
        mergedlistSample=list(kTails.stateSample) 
        
        for i in range(0,len(kTails.stateFA)):
            #tmpDictFA[i]=sequence[i]  
            for ind in kTails.stateFA:
                if check_equivalence(sequence[i:1+i],sequence[ind+1+i:ind+1+1+i]):       
                    kTails.nodelistSample.append(set([i,ind+1+i+1]))
                    if i in mergedlistSample: 
                        mergedlistSample[ind+i+1]=i
                        
    
    
    def do_kTailEquivCheck(self,k,seq,flag):

        #Note: at k == 0, all "states" should be considered equal, but an
        #event-based model cannot express this, thus the assert.
        assert(k>0)
        
        getUniqueStatesFromTrace1=set()
        sequence=[]
        
        kTails.state=[]
        kTails.nodelist=[[]]
        kTails.mergedlist=[]
        kTails.strEquiv=[]
        
        #Get final unique states from each trace
        kTails.getUniqueStates1=set()
        kTails.transDict1={}
        kTails.mapping={}
        #samplealphabet=set()

        #kTails.stateMap2={}
        #isMultitrace=False 
        if type(seq) is dict:
            
            if len(seq)>1:
                for k1,v1 in seq.items():
                    if k1==1:
                        sequence=v1 #list(seq) #A list containing sequences of traces
                    
            elif len(seq)==1:
                for ks,vs in seq.items():
                    if ks==1:
                        sequence=vs #list(seq) #A list containing sequences of traces
            
        elif type(seq) is list:
            sequence=seq
            self.FiniteAutomata(sequence)
        
        
            
        for x in range(0,len(sequence)+1-k):
            kTails.state.append(x)
            
        kTails.mergedlist=list(kTails.state) 

        
        for s in kTails.mergedlist:
            getUniqueStatesFromTrace1.add(s)
                                
        for i in range(0,len(kTails.state)):
            tmpDict[i]=sequence[i]  
            for ind in kTails.state:
                #check that the next sequence of k-length strings is not empty
                #Here assume that the order of the sequence is important 
                if (len(sequence[ind+1+i:ind+k+1+i])<k):
                    pass
                elif ind==None:
                    pass
                else:
                    if check_equivalence(sequence[i:k+i],sequence[ind+1+i:ind+k+1+i]):       
                        kTails.nodelist.append(set([i,ind+1+i]))
                        #Check state i in the merged list
                        #This captures the transitivity of states
                        #That is if s0-->s1 and s1-->s2, then s0-->s3,therefore s0,s1 and s2 are equal states                        
                        if i in kTails.mergedlist: 
                            kTails.mergedlist[ind+i+1]=i
                            #if i not in tMap:
                                #tMap[i]=sequence[i] #add state as key and transition as value to dictionary
                                #tDict.append(str(i)-sequence[i])
                            #Group the equivalent states together into sets 
                            print 'Trace 1(t1): '+ str(kTails.state.index(i))+str(sequence[i:k+i]) + '<-->' + 'State '+ str(kTails.state[ind+i+1]) + \
                                str(sequence[ind+1+i:ind+k+1+i]) + \
                                "-->equivalent strings identified for states: (" + \
                                str(i) +"," + str(ind+1+i) +") when k=" + str(k) 
                                               
                            kTails.strEquiv.append('Trace 1(t1): '+ str(kTails.state.index(i))+str(sequence[i:k+i]) + '<-->' + 'State '+ str(kTails.state[ind+i+1]) + \
                                str(sequence[ind+1+i:ind+k+1+i]) + \
                                "-->equivalent strings identified for states: (" + \
                                str(i) +"," + str(ind+1+i) +") when k=" + str(k) +'\n')
            
        print 'Trace 1: tmpDict ' + str(tmpDict)
        #if isMultitrace:
        #    print 'Trace 2: tmpDict2 ' +str(tmpDict2)
        print 'Trace 1:Initial States ' + str(kTails.state)
        #if isMultitrace:
        #    print 'Trace 2:Initial States ' + str(kTails.state2)
        print 'Trace 1:Equivalent States Identified' + str(group_States(kTails.nodelist)) 
        #if isMultitrace:
        #     print 'Trace 2:Equivalent States Identified' + str(group_States(kTails.nodelist2))           
        print 'Trace 1:Merged States  ' + str(kTails.mergedlist)
        #if isMultitrace:
        #    print 'Trace 2:Merged States  ' + str(kTails.mergedlist2)    
        print '***********************************************************************************************************************************************************************************'

        #print 'old values'
        #print 'unique states: ' + str(getUniqueStatesSample)
        #print 'Aplhabet: ' + str(alphabet)
        #print 'Transition Map: ' + str(sampleTransitionmapping)
        kTails.alphabet=[]
        if flag==0:
            getUniqueStatesSample.clear()
            #alphabet.clear()
            #transDictSample={}
            sampleTransitionmapping.clear()  
            for val1 in kTails.mergedlist:
                getUniqueStatesSample.add(int(val1))
            print 'Unique States in Sample Trace: ' + str(getUniqueStatesSample)
        
                         
            current = None
            nxt = None
            index=0
 
            while (index+1)<len(kTails.mergedlist):
                current=kTails.mergedlist[index]
                nxt=kTails.mergedlist[index+1]
                for k,v in tmpDict.items():
                    if current==k:
                        sampleTransitionmapping[(current,v)]=nxt#.append(str(current) +'-->'+ str(nxt))
                index+=1        
                                
            print 'Sample Transition Mapping:' + str(sampleTransitionmapping)
            
            #alphabet.clear()#clear any existing alphabets in the list
            samplealphabet.clear()
            
            for k in sampleTransitionmapping.iterkeys():
                p,q=k
                kTails.alphabet.append(q)
            #Do a shallow copy of the alphabet and store it in separate set for comparing with actual input alphabet
            for e in kTails.alphabet:
                samplealphabet.add(e)
                
            print 'Alphabet in Sample Trace:' + str(samplealphabet)
        else:
            for val1 in kTails.mergedlist:
                kTails.getUniqueStates1.add(int(val1))
            print 'Unique States in Trace: ' + str(kTails.getUniqueStates1)
            
            
            for g in kTails.getUniqueStates1:
                for tmpk,tmpv in tmpDict.items():
                    if g==tmpk:
                        kTails.transDict1[g]=tmpv

            
            for k,v in kTails.transDict1.items():
                kTails.alphabet.append(v)
                
            print 'Alphabet in Input Trace:' + str(kTails.alphabet)
            
        kTails.mapping=transitionMapping(kTails.mergedlist)
        
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        
        kTailG=kTailFSMGraph('FSM')
        #kTailG.generateStateTransition(kTails.mergedlist,tmpDict,stateAliasMapList,0)
        if flag==0:
            kTailG.generateStateTransition(kTails.mergedlist,tmpDict,'sample')
        elif flag==1:
            kTailG.generateStateTransition(kTails.mergedlist,tmpDict,'ktail')
        
        tmpDict.clear() #clear the contents the tmp dictionary for processing different set of inputs
        
    if __name__ == "__main__":
        pass
    
class kTailFSMGraph(object):
    mapping=[]
    stateMap={}
    sampleStatemap={}
    transDict={}
    getUniqueStates = set()
    alphabetfromtrace=OrderedDict()
    samplendfaloginfor=[]
    ndfaloginfor=[]
    accepting_states=set()
    def __init__(self, params):
        pass
        '''
        Constructor
        ''' 
    def mapping(self):
        self.mapping=[]
        return self.mapping
    
    #def stateMap(self):
    #    self.stateMap={}
    #    return self.stateMap
    
    def transDict(self):
        self.transDict={}
        return self.transDict
    
    def getUniqueStates(self):
        self.getUniqueStates=set()
        return self.getUniqueStates
    
    def duplicate_dictionary_check(self,statemap,specific_word=''):
        initial_state=None
        next_states=set()
        label=''
        #Not that in this function, we only check for the minimal existence
        #of NDFA with a state having two transitions with same label which makes the automata non-deterministic.
        #There could be more than one NDFA transitions for a single.
       
        for k,d in statemap.items(): #embedded dictionary havig value (d) as an embedded dictionary
            for key_a,value_a in d.items():
                for key_b,value_b in d.items():
                    if key_a == key_b:
                        break
                    if (value_a==value_b):
                        if specific_word:
                            if str(specific_word) == str(value_a):
                                next_states.add(key_a)
                                next_states.add(key_b)
                                label=value_a
                                initial_state=k
                                return 'Non-Deterministic Path detected at State: '+str(initial_state) + \
                                        ' [Label='+label +'] Next Transitions States:['+str(next_states)+'] Please check the log for details'
                                
                                    
        return

    def generateStateTransition(self,loadEquiState,tmpDictx,dotFile):
        ktailx=loadEquiState
        
        if len(ktailx)==0:
            pass
        
        #Identify unique states from the merged state list
        kTailFSMGraph.getUniqueStates = set()
        
        for val in ktailx:
            kTailFSMGraph.getUniqueStates.add(val)
        
        print 'unique states'+ str(kTailFSMGraph.getUniqueStates)
        
        #Dictionary to keep track of the state and its assocated transition labels
        kTailFSMGraph.transDict={}
        for g in kTailFSMGraph.getUniqueStates:
            for tmpk,tmpv in tmpDictx.items():
                if g==tmpk:
                    kTailFSMGraph.transDict[g]=tmpv
                    
        print 'transDict' + str(kTailFSMGraph.transDict)
        
        #Create a list of mapping combinations identified from the state merged list
        #Example: [0,1,1,3,4] ==>[0-->1,1-->1,1-->3,3-->4]
        
        current = None
        nxt = None
        index=0
        kTailFSMGraph.mapping=[]
        while (index+1)<len(ktailx):
                current=ktailx[index]
                nxt=ktailx[index+1]
                kTailFSMGraph.mapping.append(str(current) +'-->'+ str(nxt))
                index+=1
         
        print 'mapping' + str(kTailFSMGraph.mapping)
        
        #This dictionary stores transition of each state
        #A state may have multiple transitions.
        #Example: State 0: may have a or more transitions to itself and another transition to other state
        
        kTailFSMGraph.stateMap={}
        kTailFSMGraph.sampleStatemap={}
        print kTailFSMGraph.transDict
        for td,tv in kTailFSMGraph.transDict.items():
            #Intialize the embedded dictionary with empty string for each state
            if dotFile=='sample':
                kTailFSMGraph.sampleStatemap[td]={}
            elif dotFile=='ktail':
                kTailFSMGraph.stateMap[td]={} #The embedded dictionary stores the next transition state with the transition label as the key.
            
        for z in kTailFSMGraph.getUniqueStates:
            for e,f in kTailFSMGraph.transDict.items():
                if z==e:
                    for m in kTailFSMGraph.mapping:
                        st=[int(s) for s in m.split('-->') if s.isdigit()] #extract digits in a mapping entry
                        if str(z)==str(st[0]) and str(z)==str(st[1]):
                            if dotFile=='sample':
                                kTailFSMGraph.sampleStatemap[z][int(st[0])]=f
                            else:
                                kTailFSMGraph.stateMap[z][int(st[0])]=f
                            #Check if the transition from the current node
                            #to the next node is the same as the self-transition on current node
                            #If so then we assign and arbitrary label-as it might cause non-deterministic fsm
                        elif str(z)!=str(st[1]) and str(z)==str(st[0]):
                            if dotFile=='sample':
                                kTailFSMGraph.sampleStatemap[z][int(st[1])]=f
                            else:
                                kTailFSMGraph.stateMap[z][int(st[1])]=f
                            
        print 'Test Input Trace Map'+str(kTailFSMGraph.stateMap)
        print 'Sample Input Trace Map'+str(kTailFSMGraph.sampleStatemap)
        
        #Look for non-determistic paths in the traces for the sample input.
        
        if dotFile=='sample':
            print 'Checking for non-deterministic paths in Sample Trace Automata:'
            kTailFSMGraph.samplendfaloginfor.append('Checking for non-deterministic paths in Sample Trace Automata:')
            for k,v in kTailFSMGraph.transDict.items():
                if self.duplicate_dictionary_check(kTailFSMGraph.sampleStatemap,str(v))==None:
                    pass
                else:
                    kTailFSMGraph.samplendfaloginfor.append('==>'+str(self.duplicate_dictionary_check(kTailFSMGraph.sampleStatemap,str(v))))
                    print self.duplicate_dictionary_check(kTailFSMGraph.sampleStatemap,str(v))
                    tkMessageBox.showinfo("Non-deterministic FA", self.duplicate_dictionary_check(kTailFSMGraph.sampleStatemap,str(v)))
        
        elif dotFile=='ktail':
            kTailFSMGraph.ndfaloginfor=[] #re
            print 'Checking for non-deterministic paths in Input Trace Automata:'
            kTailFSMGraph.ndfaloginfor.append('Checking for non-deterministic paths in Input Trace Automata:')
            #print 'alpa'+str(alphabet)
            for k,v in kTailFSMGraph.transDict.items():
                #print self.duplicate_dictionary_check(kTailFSMGraph.stateMap,str(v))
                if self.duplicate_dictionary_check(kTailFSMGraph.stateMap,str(v))==None:
                    pass
                else:
                    kTailFSMGraph.ndfaloginfor.append('==>'+str(self.duplicate_dictionary_check(kTailFSMGraph.stateMap,str(v))))
                    print self.duplicate_dictionary_check(kTailFSMGraph.stateMap,str(v))
                    #tkMessageBox.showinfo("Non-deterministic FA", self.duplicate_dictionary_check(kTailFSMGraph.stateMap,str(v)))
                    
           
        #Here we appy the state transitions to create a finite state machine
        
        ktailFSM = FiniteStateMachine('K-TAIL')
        kTailFSMGraph.alphabetfromtrace.clear()
        tmpstateMap={}
        
        #make a shallow copy of the state map dictionaries
        if dotFile=='sample':
            tmpstateMap=kTailFSMGraph.sampleStatemap.copy() 
        elif dotFile=='ktail':
            tmpstateMap=kTailFSMGraph.stateMap.copy()
            
        for nx,kvx in tmpstateMap.items():
                #n=[State(s) for s in list(getUniqueStates)]
                for c in kvx:
                    State(nx).update({kvx[c]:State(c)})
                    print 'State Transition: ' +str(nx) + '-->'+str(c) + '[label='+kvx[c] +']'
                    kTailFSMGraph.alphabetfromtrace[(nx,kvx[c])]=c
                #Define initial state    
                if nx==0:
                    nx=State(0, initial=True)
                #Define acceptings states for the state machine
                if dotFile=='sample':
                    for a in kTailFSMGraph.accepting_states:
                        if a==nx:
                            nx=State(a,accepting=True)
        #clear the the tmp states map after the operation
        tmpstateMap.clear()
        #Create a state machine
        
        print '------------------------------------------------------------------------------------'
        
        try:                
            graph=get_graph(ktailFSM)
            if graph!=None:#Check if there is existing graph data 
                graph.draw('../graph/'+dotFile+'.png', prog='dot')
            else:
                pass
        except GraphvizError:
            tkMessageBox.ERROR
            
        print '-------------------------------------------------------------------------------------'
    if __name__ == "__main__":
        pass
    
