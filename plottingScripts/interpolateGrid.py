import numpy as np
import scipy.interpolate


def interpolateGridDictionary(dictionary1, dictionary2=0, withZeros=0):

	x =   list( zip( *dictionary1.keys())[0]     )  
	y =   list( zip( *dictionary1.keys())[1]     )  
	z =   list( zip( *dictionary1.values())[0]   ) 
	zSR = list( zip( *dictionary1.values())[1]   ) 

	

	if dictionary2:
		meffx =   list( zip( *dictionary2.keys())[0]     )  
		meffy =   list( zip( *dictionary2.keys())[1]     )  
		meffz =   list( zip( *dictionary2.values())[0]   ) 
		meffzSR = list( zip( *dictionary2.values())[1]   ) 

		zminusmeffz = [tmpx-tmpy for tmpx,tmpy in  zip(z,meffz)  ]

		z = zminusmeffz

	if withZeros:
		for thing in [400+10*i for i in xrange(59) ]+[1200]:
			x.append(thing)
			y.append(thing)
			z.append(0)

		for thing in [400+10*i for i in xrange(59) ]:
			x.append(thing)
			y.append(1200)
			z.append(0)


		# for thing in [400+10*(i+1) for i in xrange(38) ]:
		# 	x.append(400)
		# 	y.append(thing)
		# 	z.append(0)

	else:
		for thing in [400,1200 ]:
			x.append(thing)
			y.append(thing)
			z.append(0)

	x.append(1800)
	y.append(1200)
	z.append(0)

	x = np.array(x)
	y = np.array(y)
	z = np.array(z)

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
	if dictionary2:
		rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
	else:
		rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
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

	x.append(1800)
	y.append(1200)
	z.append(0)

	x = np.array(x)
	y = np.array(y)
	z = np.array(z)






	xi, yi = np.linspace(x.min(), x.max(), 100), np.linspace(y.min(), y.max(), 100)
	xi, yi = np.meshgrid(xi, yi)

	rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
	zi = rbf(xi, yi)

	return x,y,z,xi,yi,zi

