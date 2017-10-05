import random
import copy

import settings


class ControlSignals():
    def __init__(self, intersection):
        self.intersection = intersection
        self.flipMultiplier = random.random()
        self.phaseOffset = 100 * random.random()
        self.time = self.phaseOffset
        self.stateNum = 0
        self.states = [
            ['L', '', 'L', ''],
            ['FR', '', 'FR', ''],
            ['', 'L', '', 'L'],
            ['', 'FR', '', 'FR']
        ]
        self.STATE = {'RED': 0, 'GREEN': 1}

    def copy(self):
        return copy.deepcopy(self)

    @property
    def flipInterval(self):
        return (0.1 + 0.05 * self.flipMultiplier) * settings.setDict['lightsFlipInterval']

    def _decode(str):
        state = [0, 0, 0]
        if 'L' in str:state[0] = 1
        if 'F' in str:state[1] = 1
        if 'R' in str:state[2] = 1
        return state

    @property 
    def state(self):

      stringState = self.states[self.stateNum % len(self.states)]
      if len(self.intersection.roads) <= 2:
          stringState = ['LFR', 'LFR', 'LFR', 'LFR']

      return [self._decode(x) for x in stringState]

    def flip(self):
        self.stateNum += 1

    def onTick(self, delta):
        self.time += delta
        if self.time > self.flipInterval:
          self.flip()
          self.time -= self.flipInterval
