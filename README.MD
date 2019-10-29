PROJECT:
Integrate Answer Set Programming (ASP) with a MDP to enable efficient problem solving. Problem to solve here will be moving 'objects' between 'people' using a single virtual robot, where each actor (people or robot) in the domain can only hold one object at a given time, and there will always be at least one actor with no object. This will be done on a grid world with obstacles, where each actor will be randomly placed at a point within the world.
ASP will be used for both planning the best logical order for moving objects around the grid between actors, as well as figuring out available minimal routes to perform each plan.
MDP will be used for determining which plan and route combination is optimal for performing the task.

I plan to have experimental manipulations be in the amount of reward given, and the discount, size of grid, and number of people and objects in the domain. I plan to measure time taken (as I noticed the SPARC system can be quite slow) to assess how efficient it is, as well as whether the optimal route is taken each time (although I am not certain how to assess this, yet).

The ASP code is mostly ready (as well as a python script for generating a grid in ASP logic, but not with obstacles yet), however currently I have not started writing the MDP, as I am not sure if this is the best method. I would like to use some form of reinforcement learning instead, but I (currently) cannot think of a way to implement this.

I would also like to add some uncertainty in, to make it more realistic, however I am not sure if this is necessary.
