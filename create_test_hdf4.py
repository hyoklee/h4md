from pyhdf.SD import SD, SDC
import numpy as np

# Create a new HDF4 file
hdf = SD('test_data.hdf', SDC.WRITE | SDC.CREATE)

# Set some global attributes using the attr().set() method
hdf.attr('author').set(SDC.CHAR8, 'Test User')
hdf.attr('description').set(SDC.CHAR8, 'Sample HDF4 file for testing h4md')
hdf.attr('date_created').set(SDC.CHAR8, '2025-05-10')

# Create a simple dataset
data = np.arange(20).reshape(4, 5)
sds = hdf.create('sample_data', SDC.FLOAT32, (4, 5))
sds.data[:] = data

# Add attributes to the dataset using the attr().set() method
sds.attr('units').set(SDC.CHAR8, 'meters')
sds.attr('valid_range').set(SDC.FLOAT32, [-999.0, 999.0])
sds.attr('scale_factor').set(SDC.FLOAT32, 1.0)

# Create another dataset with different type
temps = np.random.normal(15, 5, (10, 10))
temp_sds = hdf.create('temperatures', SDC.FLOAT64, (10, 10))
temp_sds.data[:] = temps
temp_sds.attr('units').set(SDC.CHAR8, 'celsius')
temp_sds.attr('description').set(SDC.CHAR8, 'Random temperature measurements')

# Close the file
hdf.end()
