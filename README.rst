Introduction
============

This is a simple python simulator that simulates gravity in a 2D universe of balls and displays the evolution. A video example can be found here_.

Quick Start
===========

For quick start clone this repository and enter the gravitysimulator directory and start your python repl, then either: ::

    from example import Examples
    Examples.static_identical_planets_example()

or explicitly: ::

    from simulate import *
    Simulator([EulerMethodGravityEvolution()], [MergeCollision(), StarFormation()], Universe.star_planet_system(),Iterations(200)).run()

Core Logic
==========

This is the core logic from the simulator which shows how things fit together: ::

    def run(self):
        """Runs the simulation.

        Psuedocode:
            1) Check whether the simulation should keep keep running.
            2) Evolves the universe one step.
            3) Resolves the universe after the evolution.
            4) Redraws the universe.
            5) Next iteration.
        """
        while self._termination_condition.keep_running(self._universe):
            for evolution_policy in self._evolution_policies:
                evolution_policy.evolve(self._universe)
            for resolution_policy in self._resolution_policies:
                resolution_policy.resolve(self._universe)
            self._universe.draw()
        self._universe.close()

Classes
=======

Universe: The universe is represented by a collection of points. Also contains rendering logic.

Point: Represents object in the universe with a 2D position vector, 2D velocity vector, mass, radius, and whether or not the point is a star.

Vector2D: 2D vector with overridden operators that work with other vectors or numerical types.

Simulator: Brings all the pieces together and simulates the evolution of the universe.

Iterations: Termination condition that halts the 
simulation after the specified number of iterations.

EulerMethodGravityEvolution: Evolution policy that moves points according to a discrete approximation of their gravitational acceleration at different steps.

MergeCollision: Resolution policy that merges points in a way that conserves mass, momentum, and 2D area.

StarFormation: Resolution policy that converts points to stars if their_mass > threshold_mass.

Serialize: Collection of static methods for serializing objects.


Dependencies
============

While this has been tested exclusively with Python 2.7.5, it should work on all 2.* versions. It also has dependencies on jsonpickle and pygame:

-pygame = '1.9.2pre'

-jsonpickle = '0.9.2'


TODO
====

- Smoother handling of closing/keyboard interrupts etc

- Pausing and Manual Step by Step Iteration

- Robust Playback

- Runge-Kutta Gravity Evolution

- Port evolution policy to C via Cython

.. _here: https://youtu.be/gjImA0FkMOc?t=1s