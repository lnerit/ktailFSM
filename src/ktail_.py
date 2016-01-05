'''
Created on 15/12/2015

@author: lenz l nerit
'''
import sets
from itertools import combinations

class kTails(object):
    '''
    This class implements the k-tails algorithm to compare equivalent states
    and merge them before a minimal fsm is produced
    '''
    #trace=['A','B','C','A','B','C','A','B','C','A','B','C']
    k=3 # set default value to 3  but overwritten with user input
    
    def __init__(self, params):
        '''
        Constructor
        '''     
    def do_kTailEquivCheck(self,kv,seq):
        sequence=list(seq)
        state=[]
        nodelist=[[]]
        
        while True:
            response=raw_input("Please enter a value for k: ");
            if str(response)=="" or int(response)>len(sequence) or int(response)<=0:
                    print 'A valid value for k required'
                    continue
            else:
                break
                
        k=int(response)
        for x in range(0,len(sequence)+1-k):
            state.append(x)
        mergedlist=list(state) 
        for i in range(0,len(state)+1):  
            for ind in state:
                #check that the next sequence of k-length strings is not empty
                #Here assume that the order of the sequence is important
                                
                if (len(sequence[ind+1+i:ind+k+1+i])<k):
                    pass
                elif ind==None:
                    pass
                else:
                    if sequence[i:k+i]==sequence[ind+1+i:ind+k+1+i]:       
                        nodelist.append(set([i,ind+1+i]))
                        
                        #Check state i in the merged list
                        #This captures the transitivity of states
                        #That is if s0-->s1 and s1-->s2, then s0-->s3,therefore s0,s1 and s2 are equal states                        
                        if i in mergedlist: 
                            mergedlist[ind+i+1]=i
                            #Group the equivalent states together into sets                 
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
                                   
                        print 's'+ str(state.index(i))+str(sequence[i:k+i]) + '<-->' + 's'+ str(state[ind+i+1]) + \
                                str(sequence[ind+1+i:ind+k+1+i]) + \
                                "-->equivalent strings identified for states: (" + \
                                str(i) +"," + str(ind+1+i) +") when k=" + str(k)
                        
        
    
        print '---------------------------------------------------------------------------------------------------'         
        try:
            if len(sets)==0:
                pass
            else:
                print 'Equivalent States ' + str(sets)
        except:ValueError
            
                            
        print 'Initial States ' + str(state)
        print 'Merged States  ' + str(mergedlist)                   
        print '***************************************************************************************************'
        return mergedlist        
    #if __name__ == '__main__':
    #    do_kTailEquivCheck(None,k, trace)         