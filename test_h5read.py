from ORSModel import createChannelFromNumpyArray
# from ORSModel.ors import DimensionUnit
import sys
import numpy as np
import h5py


FILE = '/data/mct/19068d/recon_DT_wood_5X_18keV_GRcopy.h5'
# DT used /data/mct/20742/recon_05_r2_6158b_17keV_4p5x.h5 - volume data is at /MCT/DATA

# The Dragonfly method createChannelFromNumpyArray accepts only these Numpy data types:
# np.int8, np.uint8, np.int16, np.uint16, np.int32, np.uint32 and np.float32

with h5py.File(FILE, 'r') as f:
    data = f['/data']
    # data = f['/data'][:].astype(np.float16)
    # data = f['/data'].astype(np.float16)[:]
    # print(data.shape, data.dtype, sys.getsizeof(data))

    # rescale for nominally +ve data?
    # data = (data * np.iinfo(np.uint8).max / data.max()).astype(np.uint8)
    data = data[:]
    # x_spacing = f['/mct/data/voxel_size_x']
    # y_spacing = f['/mct/data/voxel_size_y']
    # z_spacing = f['/mct/data/voxel_size_z']

channel = createChannelFromNumpyArray(data)
channel.setTitle('Blah')
# channel.setXSpacing(x_spacing)
# channel.setYSpacing(y_spacing)
# channel.setZSpacing(z_spacing)
#channel.setDimensionUnit(unit)
channel.publish()