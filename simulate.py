from random import randint
from pygame import display, draw, event, QUIT
from math import sqrt, pi, pow
from itertools import combinations
from sys import exit
import jsonpickle as json

###################################
###
### State Classes
###
###################################

class Universe(object):
    """A collection of points representing the state of the univeres.

    Attributes:
        _points: list of Points representing state of the Universe.
    """

    SIZE = 640 # size (number of pixels in respective dimension) of the screen
    NOT_STAR_COLOR = (100, 100, 100)  # grey
    STAR_COLOR = (255,255,0) # yellow
    BACKGROUND_COLOR = (0, 0, 0) # black

    def __init__(self, points):
        self._points = points
        self._surface = None

    def __repr__(self):
        return "\nUniverse(%s)" % (str(self._points))
    
    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = points

    def remove(self, point):
        self._points.remove(point)

    def draw(self):
        """Draws the universe on a screen.

        Draws a black background which overwrites the existing screen. Then
        renders a hollow circle for each point in points. If the point is a star
        it is colored yellow, otherwise the point is colored gray. At any point
        the user can press the exit button and the program will exit.
        """
        if (not self._surface):
            self._surface = display.set_mode((self.SIZE, self.SIZE))
        self._surface.fill(self.BACKGROUND_COLOR)
        for point in self.points:
            color = self.NOT_STAR_COLOR
            if (point.star):
                color = self.STAR_COLOR
            draw.circle(self._surface, color, point.position.round.tuple, point.radius, 1)
            display.flip()
            for e in event.get():
                if e.type == QUIT:
                    exit()

    @staticmethod
    def random(number_points):
        """Generates random universe.

        Generates a list of "number_points" points with attributes that are
        drawn randomly.
        """
        points = []
        sqrt_size = int(sqrt(Universe.SIZE))
        for i in xrange(number_points):
            position = Vector2D(randint(0, Universe.SIZE), randint(0, Universe.SIZE))
            velocity = Vector2D(randint(-3, 3), randint(-Universe.SIZE / 30, Universe.SIZE / 30))
            mass = randint(Universe.SIZE / 30, Universe.SIZE)
            radius = randint(Universe.SIZE / 100, Universe.SIZE / 30)
            points.append(Point(position, velocity, mass, radius, star=False))
        return Universe(points)

    @staticmethod
    def star_planet_system():
        """Generates a universe with a central star and a spirally orbiting
        planet.
        """
        star_position = Vector2D(Universe.SIZE / 2)
        star_velocity = Vector2D.zero()
        star_mass = Universe.SIZE * 10
        star_radius = 8
        star = Point(star_position, star_velocity, star_mass, star_radius, True)
        planet_1_position = Vector2D(Universe.SIZE / 3.0)
        planet_1_velocity = Vector2D(4,-4)
        planet_1_mass = Universe.SIZE/1000
        planet_1_radius = 2
        planet_1 = Point(planet_1_position, planet_1_velocity, planet_1_mass, planet_1_radius, False)
        return Universe([star, planet_1])

    @staticmethod
    def static_identical_planets(number_points):
        """Generates a universe with a "number_points" points with identical 
        mass and zero velocity.
        """
        points = []
        sqrt_size = int(sqrt(Universe.SIZE))
        for i in xrange(number_points):
            position = Vector2D(randint(0, Universe.SIZE), randint(0, Universe.SIZE))
            velocity = Vector2D.zero()
            mass = 150
            radius = 10
            points.append(Point(position, velocity, mass, radius, star=False))
        return Universe(points)

class Point(object):
    """Represents a 2D ball in space.

    Attributes:
        _position: 2D vector of position coordinates.
        _velocity: 2D vector of velocity coordinates.
        _mass: mass of ball
        _radius: radius of ball (in pixels)
        _star: boolean
    """

    def __init__(self, position, velocity, mass, radius, star):
        self._position = position
        self._velocity = velocity
        self._mass = mass
        self._radius = radius
        self._star = star

    def __repr__(self):
        return "\nPoint(%s, %s, %d, %d, %d)" % (str(self._position), str(self._velocity), self._mass, self._radius, self._star)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, velocity):
        self._velocity = velocity

    @property
    def star(self):
        return self._star

    @star.setter
    def star(self, star):
        self._star = star

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, mass):
        self._mass = mass

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = radius

    @property
    def area(self):
        return pi * pow(self.radius, 2)

    @staticmethod
    def radius_from_area(area):
        """
        Args:
            area: some area.

        Returns:
            The radius corresponding to the "area".
        """
        return int(sqrt(area / pi))

class Vector2D(object):
    """2D vector.

    Attributes:
        _x: x dimension value.
        _y: y dimension value.
        length: l2 length of vector.
        round: new vector with integer values.
        tuple: tuple (x,y) 
    """

    def __init__(self, x, y=None):
        self._x = x
        # If initialized with one value v set x = y = v.
        if y is not None:
            self._y = y
        else:
            self._y = x

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value

    # Overriden operators.
    # See Vector2DTest.test_operations in test.py for examples.
    def __repr__(self):
        return "Vector2D(%s, %s)" % (self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vector2D(-self.x, -self.y)

    def __mul__(self, other):
        if isinstance(other, (int, float, long)):
            return Vector2D(self.x * other, self.y * other)
        return Vector2D(self.x * other.x, self.y * other.y)

    def __div__(self, other):
        if isinstance(other, (int, float, long)):
            return Vector2D(self.x / other, self.y / other)
        return Vector2D(self.x / other.x, self.y / other.y)

    def __mod__(self, other):
        if isinstance(other, (int, float, long)):
            return Vector2D(self.x % other, self.y % other)
        return Vector2D(self.x % other.x, self.y % other.y)

    @property
    def length(self):
        return sqrt(pow(self.x, 2) + pow(self.y, 2))

    @property
    def round(self):
        return Vector2D(int(self.x), int(self.y))

    @property
    def tuple(self):
        return (self.x, self.y)

    @staticmethod
    def zero():
        return Vector2D(0.0,0.0)

###################################
###
### The Simulator
###
###################################

class Simulator(object):
    """The primary class of the module. The Simulator simulates a universe.

    Attributes:
        _evolutionPolicies: List of policies that evolve a universe through one
            iteration (ex. evolving the universe via gravitational accelerations
            of its constituents).
        _resolutionPolicies: List of policies that resolve a universe
            immediately after it evolves through one iteration (ex. handling 
            cases where points collide or stars need to be formed).
        _universe: The universe to simulate.
        _terminationCondition: The condition that signals when to end the
            simulation.
    """

    def __init__(self, evolutionPolicies, resolutionPolicies, universe, terminationCondition):
        self._evolutionPolicies = evolutionPolicies
        self._resolutionPolicies = resolutionPolicies
        self._universe = universe
        self._terminationCondition = terminationCondition

    def run(self):
        """Runs the simulation.

        Psuedocode:
            1) Check whether the simulation should keep keep running.
            2) Evolves the universe one step.
            3) Resolves the universe after the evolution.
            4) Redraws the universe.
            5) Next iteration.
        """
        while self._terminationCondition.keepRunning(self._universe):
            for evolutionPolicy in self._evolutionPolicies:
                evolutionPolicy.evolve(self._universe)
            for resolutionPolicy in self._resolutionPolicies:
                resolutionPolicy.resolve(self._universe)
            self._universe.draw()

    def __repr__(self):
        return "Simulator(%s, %s, %s, %s)" % (str(self._evolutionPolicies), str(self._resolutionPolicies), str(self._universe), str(self._terminationCondition))

###################################
###
### Termination Conditions
###
###################################

class Iterations(object):
    """Terminates simulation after "limit" iterations.

    Attributes:
        _limit: Limit number of iterations.
        _iteration: Number of iterations already completed.
    """

    def __init__(self, limit):
        self._limit = limit
        self._iteration = 0

    def keepRunning(self, universe):
        if (self._iteration >= self._limit):
            return False
        self._iteration += 1
        return True

    def __repr__(self):
        return "\nIterations(%r)" % (self._limit)

###################################
###
### Evolution Policies
###
###################################

class EulerMethodGravityEvolution(object):
    """Uses EulerMethod to evolve points in a universe via gravity.

    Attributes:
        _t: evolution step size.
    """

    def __init__(self, t=1):
        self._t = t

    @staticmethod
    def compute_gravity_acceleration(point, other_points):
        """Computes a vector representing the gravitational acceleration of the 
        "point" due to the "other_points".

        Args:
            point: The point whose acceleration we are computing.
            other_points: Other points that have gravitational influence on
                "point"
        Returns:
            The acceleration vector of "point".
        """
        # simpler than G = 6.67408 * pow(10,-11)
        GRAVITATIONAL_CONSTANT = 1 
        gravityVector = Vector2D.zero()
        for other_point in other_points:
            diff = point.position - other_point.position
            r = diff.length
            magnitude = (GRAVITATIONAL_CONSTANT * other_point.  mass) / pow(r, 2)
            gravityVector = gravityVector + (diff / r) *    magnitude
        return -gravityVector

    def evolve(self, universe):
        """Applies Euler's Method (to second derivative) to evolve the points
        in the provided universe.

        Args:
            universe: The universe to evolve.
   
        Mutates:
            universe: Replaces points with a new list of points that have been
            evolved by one time step according to Euler's Method, which in this
            case reduces to
                x(t) = x(t_0) + v(t_0) * t + (a(t_0) * t^2) / 2.
        """
        point_set = set(universe.points)
        new_points = []
        for point in point_set:
            acceleration = EulerMethodGravityEvolution.compute_gravity_acceleration(point, point_set - {point})
            position = point.position + point.velocity * self._t + acceleration * pow(self._t, 2) / 2
            velocity = point.velocity + acceleration * self._t
            new_points.append(Point(position, velocity, point.mass, point.radius, point.star))
        universe.points = new_points

    def __repr__(self):
        return "\nEulerMethodGravityEvolution(t=%r)" % (self._t)

###################################
###
### Resolution Policies
###
###################################

class MergeCollision(object):
    """Merges points in a universe when they collide.
    """

    def resolve(self, universe):
        """When two points are closer than the distance of their combined radii
        , this resolution policy merges them into one point, conserving mass,
        momentum, and area. Unfortunately this method searches through all pairs
        and whenever a pair is merged has to restart. In the worst case this is 
        O(n^3) (all points have to be merged) and in practice more like O(n^2) 
        (worst case for a single merge).

        Args:
            universe: The universe to revolve.
   
        Mutates:
            universe: For each collision one point is removed and the other
            point is mutated such that momentum is conserved, mass is conserved,
            and the area of the remaining point equals the area of the original
            two points.
        """
        for p1, p2 in combinations(universe.points, 2):
            if ((p1.position - p2.position).length < p1.radius + p2.radius):        
                total_mass = p1.mass + p2.mass
                center_of_mass = (p1.position * p1.mass + p2.position * p2.mass) / total_mass
                total_velocity = (p1.velocity * p1.mass + p2.velocity * p2.mass) /  total_mass
                total_radius = Point.radius_from_area(p1.area + p2.area)
                p1.position = center_of_mass
                p1.velocity = total_velocity
                p1.mass = total_mass
                p1.radius = total_radius
                universe.remove(p2)
                self.resolve(universe)
                return  

    def __repr__(self):
        return "\nMergeCollision()"

class StarFormation(object):
    """Turns points into stars if their mass is above the "threshold_mass".

    Attributes:
        _threshold_mass: Mass beyond which a point becomes a star.
    """
    def __init__(self, threshold_mass=500):
        self._threshold_mass = threshold_mass

    @property
    def threshold_mass(self):
        return self._threshold_mass

    def resolve(self, universe):
        """When a point has a mass that is greater than "_threshold_mass" it is 
        turned into a star.

        Args:
            universe: The universe to revolve.
   
        Mutates:
            universe: The "_star" field of the points in the "universe" that
            have mass that exceeds the "_threshold_mass" will be set to True.
        """
        for point in universe.points:
            if (point.mass > self.threshold_mass):
                point.star = True

    def __repr__(self):
        return "\nStarFormation(%r)" % (self._threshold_mass)

###################################
###
### Serialization
###
###################################

class Serialize(object):
    """A collection of static methods for serializing.
    """

    @staticmethod
    def to_file(to_encode, filename):
        text_file = open(filename, "w")
        text_file.write(Serialize.encode(to_encode))
        text_file.close()

    @staticmethod
    def from_file(filename):
        text_file = open(filename, "r")
        decoded = Serialize.decode(text_file.read())
        text_file.close()
        return decoded

    @staticmethod
    def encode(to_encode):
        return json.encode(to_encode)

    @staticmethod
    def decode(to_decode):
        return json.decode(to_decode)