### Begin generated header
import sys
sys.path.append(__file__ + '/../../../../../include')
import lsss
### End generated header

import h5py
import cftime
import numpy as np

# Steps:
# 1. Load a survey or check that one is loaded
# 2. Get directory where .nc files are stored
# 3. For each .raw file:
#  3.1 Load raw file
#  3.2 Find matching .nc file
#  3.3 Loop over each region in .nc file
#  3.4 Create region in LSSS using API
#  3.5 Unload raw file
#

ncFile = 'F:\\Documents\\local\\netcdf formats\\EchosounderNetCDF\\demo_mask_vlen.nc'

f = h5py.File(ncFile, 'r')

#Open the group where the data is located
interp = f['Interpretation/v1']

# Get some variables and attributes
t = interp['mask_times']
d = interp['mask_depths']

t_units = str(interp['mask_times'].attrs['units'], 'utf-8')
t_calendar = str(interp['mask_times'].attrs['calendar'], 'utf-8')

c = interp['sound_speed'][()]
c_units = interp['sound_speed'].attrs['units']

bb_upper = interp['min_depth']
bb_lower = interp['max_depth']
bb_left = interp['start_time']
bb_right = interp['end_time']

region_id = interp['id']
region_name = interp['name']
r_type = interp['region_type']
r_type_enum = h5py.check_dtype(enum=interp['region_type'].dtype)
# Convert region types into a text version
r_type_enum = dict(map(reversed, r_type_enum.items()))
r_type_name = [r_type_enum[i] for i in r_type]

# lsss/module/{EchogramModuleId}/school-mask
# takes an list of ping masks:
#[ {
#  "time" : "2018-12-13T08:40:51.217Z",
#  "depthRanges" : [ { 
#    "min" : -1000000.0,
#    "max" : 1000000.0
#  } ]
#}, {
#  "time" : "2018-12-13T08:40:53.227Z",
#  "depthRanges" : [ {
#    "min" : -1000000.0,
#    "max" : 1000000.0
#  } ]
#} ]
#
# Returns region info

# TODO: Merge together data which has the same ping times
# Think about what happens when the ping times here don't match up with the ping times in the echogram
# Only try to create regions that are within the echogram time period? Take care with 
#   regions that start before or end after the echogram time period.
# after region creation, set acoustic categories and labels.

it = np.nditer(region_id, flags=['f_index'])
while not it.finished: # loop over all regions
    print('Working on region ' + str(it[0]) + ' (type: ' + r_type_name[it.index] +', label: "' + region_name[it.index] + '")')
    region_mask = []
    dt = cftime.num2date(t[it.index], t_units, t_calendar) # convert timestamps into a useful form

    for j, ping_time in enumerate(dt): # loop over all ping times in the region        
        depthRanges = []
        for start, stop in zip(d[it.index][j][0::2], d[it.index][j][1::2]): # loop over all depth ranges in the current time
            depthRanges.append({'min': float(start), 'max': float(stop)})
    
        region_mask.append({'time': ping_time.isoformat(timespec='milliseconds') + 'Z',
                            'depthRanges': depthRanges})

    # and now send this region mask to LSSS    
    try:
        r = lsss.post('/lsss/module/PelagicEchogramModule/school-mask', json=region_mask)
        print('...created LSSS region ' + str(r['id'])) 
        # Set some attributes on the create region
        if region_name[it.index]: # set region label (aka name) if we have one
            lsss.post('/lsss/regions/selection', json={'operation': 'SET', 'ids': r['id']})
            lsss.post('/lsss/regions/label/' + region_name[it.index])
    except ValueError:
        print('...failed')
        
    it.iternext()

#close dataset
f.close()


    
    
        