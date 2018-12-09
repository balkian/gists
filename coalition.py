from soil.agents import FSM, state, default_state
from random import randint

MAX_WEALTH = 10e6

class CoalitionAgent(FSM):
  defaults = {
    'wealth': -1,
    'wealth_threshold': 1000,
  }
  
  def __init__(self, *args, **kwargs):
    super(CoalitionAgent, self).__init__(*args, **kwargs)
    if self['wealth'] == -1:
      self['wealth'] = randint(0, self.env.get('max_wealth', MAX_WEALTH))
      
  
  @default_state
  @state
  def looking_for_coalitions(self):
    for agent in self.get_agents():
      if agent['wealth'] > self['wealth_threshold']:
        self.join_coalition(agent)
    return self.idle
  
  @state
  def idle(self):
    # Do nothing
    pass
        
  def join_coalition(self, other):
    # Add your methods here, like adding edges between users...
    # You'll probably want to check if you've already joined the user first
    self.env.add_edge(self, other)
