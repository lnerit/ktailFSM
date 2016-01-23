'''
Created on 23/01/2016

@author: lenz
'''
import unittest
from src.ktail import check_equivalence, kTails, kTailFSMGraph
from src.dfa import DFA


#from src.gui import get_num 
class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_StateEquivalence(self):
        result=check_equivalence(1,1)
        self.assertEqual(result,True,"State Equivalence Failed")
        
    
    def test_kValue(self):
        kt=kTails('k-tail')
        k=kt.k
        self.assertGreater(k, 0, "Assertion Failed...k-value must be greater than 0")
        
    def check_forNonDeterministicPath(self):
        ktx=kTailFSMGraph()
        ndfa=ktx.duplicate_dictionary_check({0: {1: 'a'}, 1: {2: 'b', 7: 'b'}, 2: {3: 'c'}, 3: {4: 'd'}, 4: {0: 'e'}, 7: {0: 'c'}},'x')
        self.assertEqual(ndfa, True, "Assert Failed")
    global d
    global accepting_states
    global states
    global alphabet
    states={0,1,2,3}
    alphabet={'a','b','c','d','e'}
    transitions={(0,'a'):1,(1,'b'):2,(2,'c'):3}
    start=0
    accepting_states={3,2}
    d=DFA(states,alphabet,transitions,start,accepting_states,1) 
    
    def test_dfa(self):
        inputString='abcabc'
        for c in inputString:
            self.assertTrue(c in alphabet,"Input symbol:"+c+' not in alphabet')
                
    def test_acceptingState(self):
        #for d.accept_states in accepting_states:
        self.assertTrue(2 in accepting_states, "Assertion Failed.State not in accepting state list")
        for s in accepting_states:
            self.assertTrue(s in states, "Assertion Failed.Undefined State:"+str(s))
        
    def test_initial_state(self):
        assert d.start_state==0
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()