#!/usr/bin/python


class DFA():
    #start_state = 0;
    #accept_states = {};
    #current_state = None;
    loginformation=[]
    
    def __init__(self, states, alphabet, transition_function, start_state, accept_states,flag):
        self.states = states;
        self.alphabet = alphabet;
        self.transition_function = transition_function;
        self.start_state = start_state;
        self.accept_states = accept_states;
        self.current_state = start_state;
        self.flag=flag #flag to indicate that we are processing the test input string so, it processing information is logged [1--> 0 means sample string,1 means test string
        return;
    
    def transition_to_state_with_input(self, input_value):
        if self.flag==1:
            self.loginformation.append('Current State: '+str(self.current_state))
            self.loginformation.append('Input Symbol : ' + input_value)
        if ((self.current_state, input_value) not in self.transition_function.keys()):
            if self.flag==1:
                if self.current_state is None:
                    self.loginformation.append('No Transition function Defined for input symbol: ' + input_value )
                if input_value not in self.alphabet:
                    self.loginformation.append('Input Symbol ' + input_value + ' NOT ACCEPTED as it is not defined in the alphabet')
            self.current_state = None;
            return;
        
        self.current_state = self.transition_function[(self.current_state, input_value)];
        if self.flag==1:
            self.loginformation.append('Next State : '+ str(self.current_state))
            self.loginformation.append('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        return;
    
    def in_accept_state(self):
        if self.flag==1:
            if self.current_state in self.accept_states:
                self.loginformation.append('Current State:'+str(self.current_state) + ' ACCEPTED as it is defined in accept states list')
            else:
                self.loginformation.append('Current State:'+str(self.current_state) + ' NOT ACCEPTED as it is NOT defined in Accepting States List:['+str(self.accept_states)+']')
        return self.current_state in self.accept_states;
    
    def go_to_initial_state(self):
        self.current_state = self.start_state;
        return;
    
    def run_with_input_list(self, input_list):
        loginformation=[]
        print 'xxxxx' +str(loginformation)
        self.go_to_initial_state();
        for inp in input_list:
            self.transition_to_state_with_input(inp);
            continue;
        if self.flag==1:
            for s in self.accept_states:
                if s not in self.states:
                    self.loginformation.append('Accepting State : ' + str(s)  + ' is not defined in the States List ['+str(self.states)+']')
                    return;
        
        return self.in_accept_state();
    
    pass;


