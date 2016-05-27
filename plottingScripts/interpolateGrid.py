import numpy as np
import scipy.interpolate

from copy import deepcopy


def interpolateGridDictionary(dictionary1, dictionary2=0, withZeros=0, runUncertainty = 0):

	x =   list( zip( *dictionary1.keys())[0]     )  
	y =   list( zip( *dictionary1.keys())[1]     )  
	z =   list( zip( *dictionary1.values())[0]   ) 
	zSR = list( zip( *dictionary1.values())[1]   ) 
	if runUncertainty:
		zd1s =   list( zip( *dictionary1.values())[2]   ) 
		zu1s =   list( zip( *dictionary1.values())[3]   ) 


	# print "1441414"*100
	# print zip(z,zd1s,zu1s)

	if dictionary2:
		meffx =   list( zip( *dictionary2.keys())[0]     )  
		meffy =   list( zip( *dictionary2.keys())[1]     )  
		meffz =   list( zip( *dictionary2.values())[0]   ) 
		meffzSR = list( zip( *dictionary2.values())[1]   ) 
		if runUncertainty:
			meffzd1s =   list( zip( *dictionary2.values())[2]   ) 
			meffzu1s =   list( zip( *dictionary2.values())[3]   ) 

		zminusmeffz = [tmpx-tmpy for tmpx,tmpy in  zip(z,meffz)  ]

		z = zminusmeffz

	if withZeros:
		for thing in [400+10*i for i in xrange(89) ]+[1200]:
			x.append(thing)
			y.append(thing)
			z.append(0)
			if runUncertainty:
				zd1s.append(0)
				zu1s.append(0)

			# for offsety in [50]:
			# 	x.append(thing)
			# 	y.append(thing+offsety)
			# 	z.append(0)


		# for thing in [10*i for i in xrange(39) ]:
		# 	x.append(thing)
		# 	y.append(thing)
		# 	z.append(0)

		# for thing in [400+10*i for i in xrange(59) ]:
		# 	x.append(thing)
		# 	y.append(1200)
		# 	z.append(0)



		# for thing in [10*(i+1) for i in xrange(59) ]:
		# 	x.append(0)
		# 	y.append(thing)
		# 	z.append(0)


		# for thing in [400+10*(i+1) for i in xrange(38) ]:
		# 	x.append(400)
		# 	y.append(thing)
		# 	z.append(0)

	else:
		for thing in [400,1200 ]:
			x.append(thing)
			y.append(thing)
			z.append(0)
			if runUncertainty:
				zd1s.append(0)
				zu1s.append(0)

	x.append(1800)
	y.append(1200)
	z.append(0)

	if runUncertainty:
		zd1s.append(0)
		zu1s.append(0)

	if withZeros:
		x.append(1500)
		y.append(1200)
		z.append(0)

		if runUncertainty:
			zd1s.append(0)
			zu1s.append(0)

	x = np.array(x)
	y = np.array(y)
	z = np.array(z)
	if runUncertainty:
		zd1s = np.array(zd1s)
		zu1s = np.array(zu1s)

	# print x,y,z

	xi, yi = np.linspace(x.min(), x.max(), 100), np.linspace(y.min(), y.max(), 100)

	# import matplotlib.mlab as mlab
	# import matplotlib.tri as tri
	# print x, y
	# triang = tri.Triangulation(x, y)

	# xi,yi,zi = x,y,z

	# zi = mlab.griddata(x, y, z, xi, yi, interp='linear')
	# zi = mlab.griddata(x, y, z, xi, yi, interp='cubic')

	xi, yi = np.meshgrid(xi, yi)
	print len(x), len(y), len(z)
	# print list(x)
	# print list(y)
	# print list(z)
	if dictionary2:
		rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
	else:
		# rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
		rbf = LSQ_Rbf(x, y, z, function='linear')

	if runUncertainty>0:
		# rbf = scipy.interpolate.Rbf(x, y, zu1s, function='linear')
		rbf = LSQ_Rbf(x, y, zu1s, function='linear')
	if runUncertainty<0:
		# rbf = scipy.interpolate.Rbf(x, y, zd1s, function='linear')
		rbf = LSQ_Rbf(x, y, zd1s, function='linear')

	zi = rbf(xi, yi)

	# from scipy.interpolate import interp2d

	# xi, yi = np.meshgrid(x,y)
	# rbf = scipy.interpolate.interp2d(x, y, z)
	# zi = rbf(xi,yi)

	return (x,y,z,zSR,xi,yi,zi)



def interpolateGridArray(x,y,z, withZeros=0):

	# for thing in [400,1200,1800 ]:
	# 	x.append(thing)
	# 	y.append(thing)
	# 	z.append(0)

	print len(x), len(y), len(z)


	x,y,z = deepcopy(x), deepcopy(y), deepcopy(z)

	if withZeros:
		for thing in [400+10*i for i in xrange(59) ]+[1200]:
			x.append(thing)
			y.append(thing)
			z.append(0)

		for thing in [400+10*i for i in xrange(59) ]:
			x.append(thing)
			y.append(1200)
			z.append(0)

	else:
		for thing in [400,1200 ]:
			x.append(thing)
			y.append(thing)
			z.append(0)

	if withZeros:
		x.append(1500)
		y.append(1200)
		z.append(0)

	x.append(1800)
	y.append(1200)
	z.append(0)

	x = np.array(x)
	y = np.array(y)
	z = np.array(z)



	xi, yi = np.linspace(x.min(), x.max(), 100), np.linspace(y.min(), y.max(), 100)
	xi, yi = np.meshgrid(xi, yi)

	print len(x), len(y), len(z)
	rbf = scipy.interpolate.Rbf(x, y, z, function='cubic')
	zi = rbf(xi, yi)

	return x,y,z,xi,yi,zi

class LSQ_Rbf(scipy.interpolate.Rbf):

    def __init__(self, *args, **kwargs):
        self.xi = np.asarray([np.asarray(a, dtype=float).flatten()
                           for a in args[:-1]])
        self.N = self.xi.shape[-1]
        self.di = np.asarray(args[-1]).flatten()

        if not all([x.size == self.di.size for x in self.xi]):
            raise ValueError("All arrays must be equal length.")

        self.norm = kwargs.pop('norm', self._euclidean_norm)
        r = self._call_norm(self.xi, self.xi)
        self.epsilon = kwargs.pop('epsilon', None)
        if self.epsilon is None:
            self.epsilon = r.mean()
        self.smooth = kwargs.pop('smooth', 0.0)

        self.function = kwargs.pop('function', 'multiquadric')

        # attach anything left in kwargs to self
        #  for use by any user-callable function or
        #  to save on the object returned.
        for item, value in kwargs.items():
            setattr(self, item, value)

        self.A = self._init_function(r) - np.eye(self.N)*self.smooth
        # use linalg.lstsq rather than linalg.solve to deal with 
        # overdetermined cases
        self.nodes = np.linalg.lstsq(self.A, self.di)[0]