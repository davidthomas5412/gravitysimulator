from simulate import * 

class Examples(object):
    """A collection of examples. See simulate.py for more details.
    """

    @staticmethod
    def random_universe_example():
        Simulator([EulerMethodGravityEvolution()], [MergeCollision(), StarFormation()], Universe.random(10), Iterations(1000)).run()

    @staticmethod
    def star_planet_example():
        Simulator([EulerMethodGravityEvolution()], [MergeCollision(), StarFormation()], Universe.star_planet_system(),Iterations(1000)).run()

    @staticmethod
    def static_identical_planets_example():
        Simulator([EulerMethodGravityEvolution()], [MergeCollision(), StarFormation()], Universe.static_identical_planets(10), Iterations(1000)).run()

    @staticmethod
    def serialization_example():
        simulator = Simulator([EulerMethodGravityEvolution()], [MergeCollision(), StarFormation()], Universe.random(10),Iterations(1000))
        encoding = Serialize.encode(simulator)
        print "Encoding: \n" + encoding
        decoding = Serialize.decode(encoding)
        print "Decoding == Encoding? " + str(str(simulator) == str(decoding))


if __name__ == "__main__":
        Examples.star_planet_example()