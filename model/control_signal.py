import random
import copy
class ControlSignals():
    def __init__(self, intersection):
        self.flipMultiplier = random.random()
        self.phaseOffset = 100 * random.random()
        self.time = self.phaseOffset
        self.stateNum = 0
    def copy(self):
        return copy.deepcopy(self)
    states = [
        ['L', '', 'L', ''],
        ['FR', '', 'FR', ''],
        ['', 'L', '', 'L'],
        ['', 'FR', '', 'FR']
    ]
    STATE = {RED: 0, GREEN: 1}
    @property
    def flipInterval(self):
        return (0.1 + 0.05 * self.flipMultiplier) * settings.lightsFlipInterval
    def _decode(str):
        state = [0, 0, 0]
        if 'L' in str:state[0] = 1 
        if 'F' in str:state[1] = 1 
        if 'R' in str:state[2] = 1 
    @property 
    def state(self):
    
      stringState = self.states[self.stateNum % self.states.length]
      if self.intersection.roads.length <= 2:
        stringState = ['LFR', 'LFR', 'LFR', 'LFR']
      for x in stringState:self._decode(x)
    def flip(self):
        self.stateNum += 1

    def onTick(delta):
        self.time += delta
        if self.time > self.flipInterval:
          self.flip()
          self.time -= self.flipInterval



        