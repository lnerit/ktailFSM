'''
Created on 15/12/2015

@author: lenz
'''
MACHINES = dict()
NOOP = lambda: None
NOOP_ARG = lambda arg: None

class FSMError(Exception):
    """Base FSM exception."""
    pass

class StateError(FSMError):
    """State manipulation error."""
    
class State(dict):
    
    """State class."""

    DOT_ATTRS = {
        'shape': 'circle',
        'height': '1.2',
    }
    DOT_ACCEPTING = 'doublecircle'

    def __init__(self, name, initial=False, accepting=False, output=None,
                 on_entry=NOOP, on_exit=NOOP, on_input=NOOP_ARG, 
                 on_transition=NOOP_ARG, machine=None, default=None):
        """Construct a state."""
        dict.__init__(self)
        self.name = name
        self.entry_action = on_entry
        self.exit_action = on_exit
        self.input_action = on_input
        self.transition_action = on_transition
        self.output_values = [(None, output)]
        self.default_transition = default
        if machine is None:
            try:
                machine = MACHINES['default']
            except KeyError:
                pass

        if machine:
            machine.states.append(self)
            if accepting:
                try:
                    machine.accepting_states.append(self)
                except AttributeError:
                    raise StateError('The %r %s does not support accepting '
                                     'states.' % (machine.name, 
                                     machine.__class__.__name__))
            if initial:
                machine.init_state = self

    def __getitem__(self, input_value):
        """Make a transition to the next state."""
        next_state = dict.__getitem__(self, input_value)
        self.input_action(input_value)
        self.exit_action()
        self.transition_action(next_state)
        next_state.entry_action()
        return next_state

    def __setitem__(self, input_value, next_state):
        """Set a transition to a new state."""
        if not isinstance(next_state, State):
            raise StateError('A state must transition to another state,'
                             ' got %r instead.' % next_state)
        if isinstance(input_value, tuple):
            input_value, output_value = input_value
            self.output_values.append((input_value, output_value))
        dict.__setitem__(self, input_value, next_state)

    def __repr__(self):
        """Represent the object in a string."""
        return '<%r %s @ 0x%x>' % (self.name, self.__class__.__name__, id(self))
