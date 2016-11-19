import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
import matplotlib.pyplot as plt
import numpy as np

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'yellow'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here

        # Initialize the Q_learn dictionary
        # Iterating through all possible combinations of each dimension - (traffic light - li, oncmoing traffic - o, traffic from left - l, traffic from right - r) and each valid action
        #Setting each possible combination to [1,1,1,1] or Initializing Q to 1
        #dummy list [1,2,3,4] is choosen to keep the same lenght as the valid actions list
        

        self.Q_learn = {}

        # sample for e.g : self.Q_learn[('green', 'forward', 'forward','left', 'forward')] = [1,1,1,1]
        
   
        for li in ['green', 'red']:
            for o in [None, 'forward', 'left', 'right']:
                for l in [None, 'forward', 'left', 'right']:
                    for r in [None, 'forward', 'left', 'right']:
                        for ac in Environment.valid_actions:
                            self.Q_learn[(li, o, l, r, ac)] = [1] * len([1,2,3,4])
                            #self.Q_learn[{{input['light']:li,input['oncoming']:o,input['left']:l,input['right']:r,input[]}}]
        

        #valid_actions = [None, 'forward', 'left', 'right']

        #self.Q_learn[('red', 'forward', 'left', 'right' , 'right')] = [2] * len(Environment.valid_actions)

         # TODO: Initialize any additional variables here

           # Declaring and Initiating Learning rate
        self.a = 0.2

        # Declaring and Initiating Discount 
        self.b = 0.2
        
        # Decalring the variable to calculate the success percentage rate

        self.S = 0

        #Declaring the trial counter variable

        self.var_trial = 0

        #Declaring the variable to track sucess rate

        self.var_trial_S = {}
        

       


    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required

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

        # TODO: Update state

        #input dictionary as defined in Enviroment.py file

        #{'light': light, 'oncoming': oncoming, 'left': left, 'right': right}

        #defining the input tuple in the same order as the initial Q state


        self.state = inputs
        self.state = (inputs['light'], inputs['oncoming'], inputs['left'], inputs['right'], self.next_waypoint)
        #self.state = tuple(sorted(self.state.values()))

        # TODO: Select action according to your policy

        #maximizing Q_learn for current state
        

        max_Q_learn = self.Q_learn[self.state].index(max(self.Q_learn[self.state]))

        # taking action to maximize value of Q_learn

        action = self.env.valid_actions[max_Q_learn]
            
        

        # Execute action and get reward for the action to maximize Q_learn

        reward = self.env.act(self, action)
    

        # TODO: Learn policy based on state, action, reward


        # To asnwer first few questions
        '''
        

        # TODO: Select action according to your policy
        action = None
        action = random.choice(Environment.valid_actions)
        
        
        
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

        self.state = inputs
        self.state['next_waypoint'] = self.next_waypoint
        self.state = tuple(sorted(self.state.items()))

        '''



        # Define the next state and next action for next Utility

        next_inputs = self.env.sense(self)
        next_state = (next_inputs['light'], next_inputs['oncoming'], next_inputs['left'], next_inputs['right'], self.planner.next_waypoint())

        # Update Q_learn by the Q learn equation as dicussed in the Q learning lesson video


        # defining the old utility
        Q_learn_prev_utility = self.Q_learn[self.state][Environment.valid_actions.index(action)]

        #the next utility update based on the Utility function dicusssed in the Q learning lesson

        Q_learn_next_utility = reward + self.b * max(self.Q_learn[next_state])


        #when learning rate is 0 the new value is the othe old value, if 1 the new value totally ignore old value
 
        self.Q_learn[self.state][Environment.valid_actions.index(action)]= (1 - self.a) * Q_learn_prev_utility + (self.a * Q_learn_next_utility)
            

        # Each trial is suceesful or not : 1 - Succesful , 0 - unsuccesful: Reference : environment.py

        # at the end of each trial we see the reward, if reward > 10 means the trial is successful else trial has failed 

        if (reward >= 10):
            self.var_trial_S[self.var_trial] = 1
        else:
            self.var_trial_S[self.var_trial] = 0




        #print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}, Q_learn = {}".format(deadline, inputs, action, reward, max_Q_learn)

        print "LearningAgent.update(): deadline = {}, inputs_light = {}, inputs_oncoming = {}, inputs_left = {}, action = {}, reward = {}, Q_learn = {}".format(deadline, inputs['light'], inputs['oncoming'], inputs['left'], action, reward, max_Q_learn)

def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=.002, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line

    # Success percentage

    print "Succes percentage is: "+str(float(a.S))+" %"
    


if __name__ == '__main__':
    run()