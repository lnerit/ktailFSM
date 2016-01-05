#!/usr/bin/python
import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fsm import FiniteStateMachine, get_graph, State
#from ktail import kTails,tmpDict

#import trace

#from ktail import kTails,tmpDict

#STATES=[1,2,3,4,5,6,7,8,9,10]
trace=[]#['A','B','C','A','B','C','A','B','C','A','B','D','B','C','A','B','C','A','B','D','C','A','B','D','B','C']
k_tail_value=2
#tmpMappingDict=tmpDict
ktail = FiniteStateMachine('K-TAIL')
class kTailFSMGraph(object):
    #k_tail_valuex=2
    #tracex=[]
    #equivalentStateList=[]
    
    def __init__(self, params):
        '''
        Constructor
        '''    
    #print str(k_tail_value) + 'k'
    #print str(trace) +'tr'
    #self.trace=trace
    #self.k_tail_value=k_tail_value
    #trace=['A','B','C','A','B','C','A','B','C','A','B','D','B','C','A','B','C','A','B','D']
    #self.k_tail_value=k_tail_value
    #self.trace=trace
    def generateStateTransition(self,loadEquivalentState):
        #print k_tail_value,trace
        #kt=kTails('k-tails')
        ktailx=loadEquivalentState#kt.do_kTailEquivCheck(k_tail_value,trace)
        
        print 'transition ' + str(ktailx)
        
        if len(ktailx)==0:
            pass
        #for mv in ktailx:
        #    if mv==match_Values(ktailx):
        #        print mv
        
        #Identify unique states from the merged state list
        getUniqueStates = set()
        for val in ktailx:
            getUniqueStates.add(val)
        
        print getUniqueStates
        #Dictionary to keed track of the state and its assocated transition labels
        transDict={}
        for g in getUniqueStates:
            for tmpk,tmpv in ktail.tmpDict.items():
                if g==tmpk:
                    transDict[g]=tmpv
                    
        print 'transDict' + str(transDict)
        
        #Create a list of mapping combinations identified from the state merged list
        #Example: [0,1,1,3,4] ==>[0-->1,1-->1,1-->3,3-->4]
        current = None
        nxt = None
        index=0
        mapping=[]
        while (index+1)<len(ktailx):
                current=ktailx[index]
                nxt=ktailx[index+1]
                mapping.append(str(current) +'-->'+ str(nxt))
                index+=1
                
        print 'mapping' + str(mapping)
        
        #This dictionary stores transition of each state
        #A state may have multiple transitions.
        #Example: State 0: may have a or more transitions to itself and another transition to other state
        stateMap={}
        print transDict
        for td,tv in transDict.items():
            #for tm in mapping:
            #    stm=[int(s) for s in tm.split('-->') if s.isdigit()]
            #    if str(td)==stm[0]:
                    #stateMap[td]={ tv:' '}  #Intialize the embedded dictionary with empty string for each state
                    stateMap[td]={}                        #The embedded dictionary stores the next transition state with the 
                                            #transition label as the key.
        print  'stateMap'+ str(stateMap)
        for z in getUniqueStates:
            for e,f in transDict.items():
                if z==e:
                    for m in mapping:
                        st=[int(s) for s in m.split('-->') if s.isdigit()] #extract digits a mapping entry
                        if str(z)==str(st[0]) and str(z)==str(st[1]):
                        #if str(z)==m[-1] and str(z)==m[0]:#Check for occurance of transition to itself
                            #if m[0] not in stateMap[z]:
                            stateMap[z][int(st[0])]=f
                            #print 'x'+stateMap[z][m[-1]] + m
                            #Check if the transition from the current node
                            #to the next node is the same as the self-transition on current node
                            #If so then we assign and arbitrary label-as it might cause non-deterministic fsm
                        elif str(z)!=str(st[1]) and str(z)==str(st[0]):
                            #print stateMap[z][int(st[1])]
                            stateMap[z][int(st[1])]=f
                        #elif str(z)==str(st[1]) and str(z)!=str(st[0]): 
                        #    stateMap[z][int(st[0])]=f
        print 'statemap'+str(stateMap)
        
        #Here we appy the state transitions to create a finite state machine
        for nx,kvx in stateMap.items():
            #n=[State(s) for s in list(getUniqueStates)]
            for c in kvx:
                State(nx).update({kvx[c]:State(c)})
                print 'State: ' +str(nx) + kvx[c] +':'+str(c)
            #Define initial state    
            if nx==0:
                    nx=State(0, initial=True)    
        
        #Create a state machine
        graph = get_graph(ktail)
        graph.draw('ktail.png', prog='dot')
        print 'End of Print line'


 