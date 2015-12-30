from simulate import * 

class Examples
    """A collection of examples. See simulate.py for more details.
    """
	
	def random_universe_example():
		Simulator([EulerMethodGravityEvolution()], [MergeCollision(), StarFormation()], Universe.random(10), Iterations(1000)).run()

	def star_planet_example():
		Simulator([EulerMethodGravityEvolution()], [MergeCollision(), StarFormation()], Universe.star_planet_system(), Iterations(	1000)).run()
	
	def static_identical_planets_example():
		Simulator([EulerMethodGravityEvolution()], [MergeCollision(), StarFormation()], Universe.random(10), Iterations(1000)).run(	)
	
	def serialization_example():
		simulator = Simulator([EulerMethodGravityEvolution()], [MergeCollision(), StarFormation()], Universe.random(10), Iterations	(1000))
		encoding = Serialize.encode(simulator)
		print "Encoding: \n" + encoding
		decoding = Serialize.decode(encoding)
		print "Decoding == Encoding? " + str(str(simulator) == str(decoding))


if __name__ == "__main__":
	Examples.star_planet_example()