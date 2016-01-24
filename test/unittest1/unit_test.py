'''
Created on 23/01/2016

@author: lenz
'''

import unittest
from src.ktail import check_equivalence, kTails, kTailFSMGraph,group_States,transitionMapping
from src.dfa import DFA
from collections import OrderedDict
import coverage
from fsm import State, FiniteStateMachine, get_graph, MooreMachine

# .. call your code ..

#from src.gui import get_num 
class Test(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    #Test cases for ktail class
    global kt
    global k
    global ktfsm
    kt=kTails('k-tail')
    k=kt.k
    ktfsm=kTailFSMGraph('ktail')
    
    def test_StateEquivalence(self):
        result=check_equivalence(1,1)
        self.assertEqual(result,True,"State Equivalence Failed")
        
    def test_kValue(self):
        self.assertGreater(k, 0, "Assertion Failed...k-value must be greater than 0")
        
    def test_do_kTailEquivCheck(self):
        self.expected=[0,1,2,3,4,0,1]
        seq=['a','b','c','d','e','a','b','c']
        mergedlist=kt.do_kTailEquivCheck(k,seq,0)
        self.assertListEqual(self.expected, mergedlist, None)
        
    def test_group_States(self):
        self.expected=[set([0, 3, 5, 8]), set([1, 6, 9]), set([2, 7])]
        self.assertEquals(self.expected, group_States(self.expected), "Assert Failed")
        
    def test_transitionmapping(self):
        self.expected=[]
        self.expected=['0-->1','1-->2','2-->3']
        l= transitionMapping([0,1,2,3])
        self.assertEqual(self.expected,l,None)
        l2= transitionMapping([0,1,2,3,4])
        self.assertFalse(self.expected==l2,None)
        
    def test_duplicate_dictionary_check(self):
        statemap={0: {1: 'a'}, 1: {2: 'b', 7: 'b'}, 2: {3: 'c'}, 3: {4: 'd'}, 4: {0: 'e'}, 7: {0: 'c'}}
        tst=ktfsm.duplicate_dictionary_check(statemap, 'b')
        self.assertTrue(tst==True, None)
        tst=ktfsm.duplicate_dictionary_check(statemap, 'x')
        self.assertFalse(tst==False, None)
        statemap1={0: {1: 'a'}, 1: {2: 'b'}, 2: {3: 'c'}, 3: {4: 'd'}, 4: {0: 'e'}, 7: {0: 'c'}}
        tst=ktfsm.duplicate_dictionary_check(statemap1, 'b')
        self.assertFalse(tst==False, None)
        
    #def test_generateStateTransition(self):
    #    tmpdict=OrderedDict([(0, 'a'), (1, 'b'), (2, 'c'), (3, 'a'), (4, 'b'), (5, 'a'), (6, 'd'), (7, 'c')])
    #    mergedstates=[0, 1, 2, 0, 4, 5, 6, 7]
    #    ktfsmStatus=ktfsm.generateStateTransition(mergedstates, tmpdict, 'ktail')
    #    self.assertTrue(ktfsmStatus==True, None)
        
    #Test cases for DFA class
    
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
   
    '''
    The start state is always 0
    '''
    def test_initial_state(self):
        self.assertTrue(d.start_state==0,"Start Start must be zero")
    
    #Test cases for GUI class
    from src.gui import get_num,get_apha,loadFSMImage
    def test_get_num(self):
        from src.gui import get_num
        self.assertTrue(type(int(get_num('1-->2')))==int, "Assert Failed.Not an int type")
        
    def test_get_apha(self):
        from src.gui import get_apha
        a=get_apha('a~')
        self.assertTrue(a.isalpha(),'Assertion Failed.Not Alphabetic character found.')
    
    #def test_load_image(self):
    #    from src.gui import loadFSMImage
    #    i=loadFSMImage()
    #    self.assertTrue(i%2!=0,"Assert Failed.")
    
    #Test cases for resizeimage Class
    
    def test_resizeimage(self):
        from src.resizeimage import resizeImage
        filename='../graph/sample.png'
        factor=0.5
        ri=resizeImage(filename,factor)
        self.assertTrue(ri==None, None)
    
    #Test cases for fsm module
    from fsm import FiniteStateMachine, get_graph, State
    def test_tcp_fsm(self):
        STATES = ['LISTEN', 'SYN RCVD', 'ESTABLISHED', 'SYN SENT', 
          'FIN WAIT 1', 'FIN WAIT 2', 'TIME WAIT', 'CLOSING', 'CLOSE WAIT',
          'LAST ACK']

        tcpip = FiniteStateMachine('TCP IP')
        closed = State('CLOSED', initial=True)
        listen, synrcvd, established, synsent, finwait1, finwait2, timewait, \
        closing, closewait, lastack = [State(s) for s in STATES]
        
        timewait['(wait)'] = closed
        closed.update({r'passive\nopen': listen,
                       'send SYN': synsent})
        
        synsent.update({r'close /\ntimeout': closed,
                        r'recv SYN,\nsend\nSYN+ACK': synrcvd,
                        r'recv SYN+ACK,\nsend ACK': established})
        
        listen.update({r'recv SYN,\nsend\nSYN+ACK': synrcvd,
                       'send SYN': synsent})
        
        synrcvd.update({'recv ACK': established,
                        'send FIN': finwait1,
                        'recv RST': listen})
        
        established.update({'send FIN': finwait1,
                            r'recv FIN,\nsend ACK': closewait})
        
        closewait['send FIN'] = lastack
        
        lastack['recv ACK'] = closed
        
        finwait1.update({'send ACK': closing,
                         'recv ACK': finwait2,
                         r'recv FIN, ACK\n send ACK': timewait})
        
        finwait2[r'recv FIN,\nsend ACK'] = timewait
        
        closing[r'recv\nACK'] = timewait
        
        graph = get_graph(tcpip)
        graph.draw('tcp.png', prog='dot')
        
    def test_parkingmeter_fsm(self):
        parking_meter = MooreMachine('Parking Meter')

        ready = State('Ready', initial=True)
        verify = State('Verify')
        await_action = State(r'Await\naction')
        print_tkt = State('Print ticket')
        return_money = State(r'Return\nmoney')
        reject = State('Reject coin')
        ready[r'coin inserted'] = verify
        
        verify.update({'valid': State(r'add value\rto ticket'), 
                       'invalid': reject})
        
        for coin_value in verify:
            verify[coin_value][''] = await_action
        
        await_action.update({'print': print_tkt,
                             'coin': verify,
                             'abort': return_money,
                             'timeout': return_money})
        return_money[''] = print_tkt[''] = ready
        get_graph(parking_meter).draw('parking.png', prog='dot')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    cov = coverage.coverage()
    cov.start()
    unittest.main()
    cov.stop()
    cov.save()
    
    cov.html_report()