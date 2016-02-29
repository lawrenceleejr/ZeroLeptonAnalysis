import numpy as np
import scipy.interpolate


def interpolateGridDictionary(dictionary1, dictionary2=0):

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

	for thing in [400,1200,1800 ]:
		x.append(thing)
		y.append(thing)
		z.append(0)

	x = np.array(x)
	y = np.array(y)
	z = np.array(z)

	xi, yi = np.linspace(x.min(), x.max(), 100), np.linspace(y.min(), y.max(), 100)
	xi, yi = np.meshgrid(xi, yi)
	rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
	zi = rbf(xi, yi)

	return (x,y,z,zSR,xi,yi,zi)



def interpolateGridArray(x,y,z):

	for thing in [400,1200,1800 ]:
		x.append(thing)
		y.append(thing)
		z.append(0)

	x = np.array(x)
	y = np.array(y)
	z = np.array(z)

	xi, yi = np.linspace(x.min(), x.max(), 100), np.linspace(y.min(), y.max(), 100)
	xi, yi = np.meshgrid(xi, yi)

	rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
	zi = rbf(xi, yi)

	return x,y,z,xi,yi,zi

