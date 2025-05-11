from pyhdf.SD import SD, SDC
import numpy as np

# Create a new HDF4 file
hdf = SD('test_data.hdf', SDC.WRITE | SDC.CREATE)

# Set some global attributes
hdf.setattr('author', 'Test User')
hdf.setattr('description', 'Sample HDF4 file for testing h4md')
hdf.setattr('date_created', '2025-05-10')

# Create a simple dataset
data = np.arange(20).reshape(4, 5)
sds = hdf.create('sample_data', SDC.FLOAT32, (4, 5))
sds.data[:] = data

# Add attributes to the dataset
sds.setattr('units', 'meters')
sds.setattr('valid_range', [-999.0, 999.0])
sds.setattr('scale_factor', 1.0)

# Create another dataset with different type
temps = np.random.normal(15, 5, (10, 10))
temp_sds = hdf.create('temperatures', SDC.FLOAT64, (10, 10))
temp_sds.data[:] = temps
temp_sds.setattr('units', 'celsius')
temp_sds.setattr('description', 'Random temperature measurements')

# Close the file
hdf.end()
