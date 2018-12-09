from soil.agents import FSM, state, default_state
from random import randint

MAX_WEALTH = 2000


class CoalitionAgent(FSM):

  defaults = {
    'wealth': -1,
    'wealth_threshold': 1000,
  }

  def __init__(self, *args, **kwargs):
    super(CoalitionAgent, self).__init__(*args, **kwargs)
    if self['wealth'] == -1:
      self['wealth'] = int(randint(0, self.env.get('max_wealth', MAX_WEALTH)))


  @default_state
  @state
  def looking_for_coalitions(self):
    for agent in self.get_agents(state_id=self.looking_for_coalitions.id):
      if agent['wealth'] > self['wealth_threshold']:
        self.join_coalition(agent)
    friends = list(friend.id for friend in self.get_neighboring_agents())
    self.info('List of friends: {}'.format(friends))
    return self.idle

  @state
  def idle(self):
    # Do nothing
    pass

  def join_coalition(self, other):
    # Adill.detect.badobjectsdd your methods here, like adding edges between users...
    # You'll probably want to check if you've already joined the user first
    self.info('Joining {}'.format(other.id))
    self.env.add_edge(self, other)
