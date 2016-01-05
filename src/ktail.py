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
            #else:
            #print 'Equivalent States ' + str(sets)
            #except:ValueError
        return sets          


#This function checks for equivalent states based k-tails strings
#for two states p,q. If matched found then returns True and False otherwise
def check_equivalence(p,q):
    if p==q: 
        return True
    else:
        return False

class kTails(object):
    '''
    This class implements the k-tails algorithm to compare equivalent states
    and merge them before a minimal fsm is produced
    '''
    #trace=['A','B','C','A','B','C','A','B','C','A','B','C']
    k=3 # set default value to 3  but overwritten with user input
    
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
    
    def do_kTailEquivCheck(self,k,seq,stateAliasMapList):
        #self.k=k
        #self.seq=seq
        #Note: at k == 0, all "states" should be considered equal, but an
        #event-based model cannot express this, thus the assert.
        #assert(k>0)
        sequence=list(seq) #A list containing sequences of traces
       
        kTails.state=[]
        kTails.nodelist=[[]]
        kTails.mergedlist=[]
        kTails.strEquiv=[]
        #tmpDict=[]
        for x in range(0,len(sequence)+1-k):
            kTails.state.append(x)
            
        kTails.mergedlist=list(kTails.state) 
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
                            print 'State '+ str(kTails.state.index(i))+str(sequence[i:k+i]) + '<-->' + 'State '+ str(kTails.state[ind+i+1]) + \
                                str(sequence[ind+1+i:ind+k+1+i]) + \
                                "-->equivalent strings identified for states: (" + \
                                str(i) +"," + str(ind+1+i) +") when k=" + str(k) 
                                               
                            kTails.strEquiv.append('State '+ str(kTails.state.index(i))+str(sequence[i:k+i]) + '<-->' + 'State '+ str(kTails.state[ind+i+1]) + \
                                str(sequence[ind+1+i:ind+k+1+i]) + \
                                "-->equivalent strings identified for states: (" + \
                                str(i) +"," + str(ind+1+i) +") when k=" + str(k)+'\n')

        
        print '----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'         
        print 'tmpDict ' + str(tmpDict)
        print 'Initial States ' + str(kTails.state)
        print 'Equivalent States Identified' + str(group_States(kTails.nodelist))         
        print 'Merged States  ' + str(kTails.mergedlist)                   
        print '***********************************************************************************************************************************************************************************'
        try:
            kTailG=kTailFSMGraph('FSM')
            kTailG.generateStateTransition(kTails.mergedlist,tmpDict,stateAliasMapList,0)
        except "Error":
            tkMessageBox("Error","An error occured while processing the ktail FSM")
        
    
class kTailFSMGraph(object):
    mapping=[]
    stateMap={}
    transDict={}
    getUniqueStates = set()
    
    def __init__(self, params):
        pass
        '''
        Constructor
        ''' 
    def mapping(self):
        self.mapping=[]
        return self.mapping
    
    def stateMap(self):
        self.stateMap={}
        return self.stateMap
    
    def transDict(self):
        self.transDict={}
        return self.transDict
    
    def getUniqueStates(self):
        self.getUniqueStates=set()
        return self.getUniqueStates

    #def generateStateTransition(self,loadEquiState,tmpDictx,stateAliasList,status):
    def generateStateTransition(self,loadEquiState,tmpDictx,stateAliasList,status):
        ktailx=loadEquiState
        
        #print 'transition ' + str(ktailx)
        
        if len(ktailx)==0:
            pass
        #for mv in ktailx:
        #    if mv==match_Values(ktailx):

        
        #Identify unique states from the merged state list
        kTailFSMGraph.getUniqueStates = set()
        
        for val in ktailx:
            kTailFSMGraph.getUniqueStates.add(val)
        
        print kTailFSMGraph.getUniqueStates
        #Dictionary to keed track of the state and its assocated transition labels
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
        print kTailFSMGraph.transDict
        for td,tv in kTailFSMGraph.transDict.items():
            #for tm in mapping:
            #    stm=[int(s) for s in tm.split('-->') if s.isdigit()]
            #    if str(td)==stm[0]:
                    #stateMap[td]={ tv:' '}  #Intialize the embedded dictionary with empty string for each state
                    kTailFSMGraph.stateMap[td]={}  #The embedded dictionary stores the next transition state with the 
                    #transition label as the key.
        for z in kTailFSMGraph.getUniqueStates:
            for e,f in kTailFSMGraph.transDict.items():
                if z==e:
                    for m in kTailFSMGraph.mapping:
                        st=[int(s) for s in m.split('-->') if s.isdigit()] #extract digits a mapping entry
                        if str(z)==str(st[0]) and str(z)==str(st[1]):
                        #if str(z)==m[-1] and str(z)==m[0]:#Check for occurrance of transition to itself
                            #if m[0] not in stateMap[z]:
                            kTailFSMGraph.stateMap[z][int(st[0])]=f
                            #print 'x'+stateMap[z][m[-1]] + m
                            #Check if the transition from the current node
                            #to the next node is the same as the self-transition on current node
                            #If so then we assign and arbitrary label-as it might cause non-deterministic fsm
                        elif str(z)!=str(st[1]) and str(z)==str(st[0]):
                            #print stateMap[z][int(st[1])]
                            kTailFSMGraph.stateMap[z][int(st[1])]=f
                        #elif str(z)==str(st[1]) and str(z)!=str(st[0]): 
                        #    stateMap[z][int(st[0])]=f
        print 'statemap'+str(kTailFSMGraph.stateMap)
        
        for key,value in kTailFSMGraph.stateMap.items():
            if value==' ':
                pass
            else:
                print key,value
        
        #Here we appy the state transitions to create a finite state machine
        ktail = FiniteStateMachine('K-TAIL')
        if status==0:
            for nx,kvx in kTailFSMGraph.stateMap.items():
                #n=[State(s) for s in list(getUniqueStates)]
                for c in kvx:
                    State(nx).update({kvx[c]:State(c)})
                    print 'State Transition: ' +str(nx) + '-->'+str(c) + '[label='+kvx[c] +']'
                #Define initial state    
                if nx==0:
                        nx=State(0, initial=True)
                        #nx.DOT_ATTRS={'shape': 'octagon','height': '0.2'}
        elif status==1:
            """
            This code sectment not inplemented correctly yet
            """
            sAliasMap={}
            for nx,kvx in kTailFSMGraph.stateMap.items():
                #n=[State(s) for s in list(getUniqueStates)]
                    sAliasMap=stateAliasList.copy()
                    for saKey,saValue in sAliasMap.items():
                        #print saKey,iter(saValue).next()
                        #print iter(saValue).next()
                        print saValue
                        if nx==saKey:
                            #check for the embedded key having same state alias
                            for c in kvx:
                                if c==saKey:
                                    State(saValue).update({kvx[c]:State(iter(saValue).next())})
                                    print 'State Transition: ' +str(saValue) + '-->'+str(saKey) + '[label='+kvx[c] +']'
                    #Define initial state    
                            if saKey==0:
                                nx=State(saValue, initial=True)

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
            
        print '-------------------------------------------------------------------------------------'

    