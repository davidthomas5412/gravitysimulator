import simulate
from unittest import TestCase, main
from math import sqrt
from os import remove	

class Factory(object):
    """A collection of static methods that generate standard instances used throughout tests.
    """
    
    @staticmethod
    def get_simple_universe():
        position1 = simulate.Vector2D(1, 1)
        position2 = simulate.Vector2D(2, 2)
        position3 = simulate.Vector2D(20, 20)
        velocity = simulate.Vector2D(2, 2)
        mass = 10
        radius = 5
        star = False
        point1 = simulate.Point(position1, velocity, mass, radius, star)
        point2 = simulate.Point(position2, velocity, mass, radius, star)
        point3 = simulate.Point(position3, velocity, mass, radius, star)
        return simulate.Universe([point1, point2, point3])

    @staticmethod
    def get_simulator():
        return simulate.Simulator([simulate.EulerMethodGravityEvolution()], [simulate.MergeCollision(), simulate.StarFormation()], simulate.Universe.star_planet_system(), simulate.Iterations(10))

    @staticmethod
    def get_evolve_universe():
        position_1 = simulate.Vector2D.zero()
        velocity_1 = simulate.Vector2D.zero()
        mass_1 = 1
        radius_1 = 0
        planet_1 = simulate.Point(position_1, velocity_1, mass_1, radius_1, False)
        position_2 = simulate.Vector2D(0,4)
        velocity_2 = simulate.Vector2D.zero()
        mass_2 = 1
        radius_2 = 0
        planet_2 = simulate.Point(position_2, velocity_2, mass_2, radius_2, False)
        return simulate.Universe([planet_1, planet_2])

class Vector2DTest(TestCase):
    
    def setUp(self):
        self.v1 = simulate.Vector2D(4, 2)
        self.v2 = simulate.Vector2D(2, 1)
        self.v3 = simulate.Vector2D(2, 1)
        self.v4 = simulate.Vector2D(2, 2)
        self.v5 = simulate.Vector2D(2.1, 2.03)
        self.v6 = simulate.Vector2D(-4, -2)
        self.v7 = simulate.Vector2D(1, 2)
        self.v8 = simulate.Vector2D(3, 4)

    def test_operations(self):
        self.assertEqual(self.v2, self.v3)
        self.assertEqual(self.v1, self.v2 + self.v3)
        self.assertEqual(self.v3, self.v1 - self.v2)
        self.assertEqual(self.v1, self.v2 * self.v4)
        self.assertEqual(self.v4, self.v1 / self.v2)
        self.assertEqual(self.v1, self.v2 * 2)
        self.assertEqual(self.v2, self.v1 / 2)
        self.assertEqual(self.v4, self.v5.round)
        self.assertAlmostEqual(self.v2.length, sqrt(5))
        self.assertEqual((0, 0), simulate.Vector2D.zero().tuple)
        self.assertEqual(self.v6, -self.v1)
        self.assertEqual(self.v7, self.v1 % 3)
        self.assertEqual(self.v7, self.v1 % self.v8)


class PointTest(TestCase):

    def test_general(self):
        position = simulate.Vector2D(1, 1)
        velocity = simulate.Vector2D(2, 2)
        mass = 10
        radius = 5
        star = False
        point = simulate.Point(position, velocity, mass, radius, star)
        self.assertEqual(position, point.position)
        self.assertEqual(velocity, point.velocity)
        self.assertEqual(mass, point.mass)
        self.assertEqual(radius, point.radius)
        self.assertEqual(star, point.star)
        self.assertAlmostEqual(78.53981633, point.area)

    def test_radius_from_area(self):
        self.assertEqual(5, simulate.Point.radius_from_area(78.6))

class UniverseTest(TestCase):

    def test_remove(self):
        universe = Factory.get_simple_universe()
        universe.remove(universe.points[0])
        self.assertEqual(2, len(universe.points))

    def test_draw(self):
        Factory.get_simple_universe().draw()

class StarFormationTest(TestCase):
    
    def test_not_star_formation(self):
        star_formation = simulate.StarFormation(0)
        universe = Factory.get_simple_universe()
        star_formation.resolve(universe)
        for point in universe.points:
            self.assertEqual(point.star, True)

    def test_star_formation(self):
        star_formation = simulate.StarFormation(20)
        universe = Factory.get_simple_universe()
        star_formation.resolve(universe)
        for point in universe.points:
            self.assertEqual(point.star, False)

class MergeCollisionTest(TestCase):
    
    def test_merge_collision(self):
        merge_collision = simulate.MergeCollision()
        universe = Factory.get_simple_universe()
        merge_collision.resolve(universe)
        self.assertEqual(2, len(universe.points))
        
class IterationsTest(TestCase):
    
    def test_iterations(self):
        iterations = simulate.Iterations(20)
        universe = Factory.get_simple_universe()
        i = 0
        while (i < 20):
            self.assertTrue(iterations.keepRunning(universe))
            i += 1
        self.assertFalse(iterations.keepRunning(universe))

class SerializeTest(TestCase):

    def test_serialization(self):
        before = Factory.get_simulator()
        file_name = 'simulator.txt'
        simulate.Serialize.to_file(before, file_name)
        after = simulate.Serialize.from_file(file_name)
        self.assertEqual(str(before), str(after))
        remove(file_name)

class EulerMethodGravityEvolutionTest(TestCase):

    def test_evolution(self):
        universe = Factory.get_evolve_universe()
        evolution = simulate.EulerMethodGravityEvolution()
        evolution.evolve(universe)
        self.assertAlmostEqual(3.9375, (universe.points[0].position - universe.points[1].position).length)
        evolution.evolve(universe)
        print (universe.points[0].position - universe.points[1].position).length
        self.assertAlmostEqual(3.748, (universe.points[0].position - universe.points[1].position).length, 3)

class SimulatorTest(TestCase):

    def test_run_simulation(self):
         Factory.get_simulator().run()

if __name__ == '__main__':
    main()