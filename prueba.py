class ControlModelM2(BaseBehaviour):
  NEUTRAL = 0
  INFECTED = 1
  def step(self, now):
    if self.state['id'] == self.NEUTRAL: #Neutral
      self.neutral_behaviour()
    elif self.state['id'] == self.INFECTED: #Infected
      self.infected_behaviour()
    …
  def infected_behaviour(self):
    neutral_neighbors = self.get_neighboring_agents(state_id=0)
    for neighbor in neutral_neighbors:
      if random.random() < self.prob_infect:
        neighbor.state['id'] = self.INFECTED
