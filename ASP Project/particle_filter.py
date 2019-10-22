import motion_models as mm
import sensor_models as sm
import random
import numpy as np
from math import pi

def particle_filter(previous_particles, control, measurements, map):
    potential_particles = []
    particles_weights = []
    returned_particles = []

    #control must include previous internal coordinate?

    for i_particle in range(0,len(previous_particles)):
        particle = mm.sample_motion_model_odom(previous_particles[i_particle],control, mm.sample_norm)
        weight = sm.scan_model(measurements, particle, map)
        potential_particles.append(particle)
        particles_weights.append(weight)

    norm_weights = np.divide(particles_weights, np.sum(particles_weights))
    returned_particles_idx = np.random.choice(range(0,len(potential_particles)),len(potential_particles),True,norm_weights)
    for i in range(0,len(returned_particles_idx)):
        returned_particles.append(potential_particles[returned_particles_idx[1]])
    return returned_particles
