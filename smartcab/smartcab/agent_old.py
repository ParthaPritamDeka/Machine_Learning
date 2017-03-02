import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'yellow'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.reward = 0
        self.next_waypoint = None

        # Decalring the variable to calculate the success percentage rate

        self.S = 0

        #Declaring the trial counter variable

        self.var_trial = 0

        #Declaring the variable to track sucess rate

        self.var_trial_S = {}

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.state = None
        self.next_waypoint = None

          # Incrementing the success percentage counter before reseting the trial

        try:
           if self.var_trial_S[self.var_trial] == 1:
              self.S = self.S + 1
        except:
           pass

        # reseting the trial

        self.var_trial = self.var_trial + 1


    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

               
        # TODO: Select action according to your policy
        action = None
        action = random.choice(Environment.valid_actions)
        
        '''
        # TODO: Update state
        action_okay = True
        if self.next_waypoint == 'right':
            if inputs['light'] == 'red' and inputs['left'] == 'forward':
                action_okay = False

        elif self.next_waypoint == 'straight':
            if inputs['light'] == 'red':
                action_okay = False

        elif self.next_waypoint == 'left':
            if inputs['light'] == 'red' or inputs['oncoming'] == 'forward' or inputs['oncoming'] == 'right':
                action_okay = False

        if not action_okay:
            action = None
        '''

        self.state = inputs
        self.state['next_waypoint'] = self.next_waypoint
        self.state = tuple(sorted(self.state.items()))

        # Execute action and get reward
        reward = self.env.act(self, action)
        self.reward = self.reward + reward
        # TODO: Learn policy based on state, action, reward

         # at the end of each trial we see the reward, if reward > 10 means the trial is successful else trial has failed 

        if (reward >= 10):
            self.var_trial_S[self.var_trial] = 1
        else:
            self.var_trial_S[self.var_trial] = 0

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.002, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line

    print "Succes percentage is: "+str(float(a.S))+" %"


if __name__ == '__main__':
    run()
