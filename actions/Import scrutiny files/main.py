### Begin generated header
import sys
sys.path.append(__file__ + '/../../../../../include')
import lsss
### End generated header

from netCDF4 import Dataset, num2date

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

ncFile = 'F:\\Documents\\local\\netcdf formats\\EchosounderNetCDF\\demo_mask.nc'

dataset = Dataset(ncFile)

#Open the group where the data is located
interp = dataset.groups['Interpretation'].groups['v1']

# Get some variables and attributes
t = interp.variables['mask_times'][:]
d = interp.variables['mask_depths'][:]

t_units = interp.variables['mask_times'].units
t_calendar = interp.variables['mask_times'].calendar

c = interp.variables['sound_speed'][:]
c_units = interp.variables['sound_speed'].units

bb_upper = interp.variables['min_depth'][:]
bb_lower = interp.variables['max_depth'][:]
bb_left = interp.variables['start_time'][:]
bb_right = interp.variables['end_time'][:]

region_id = interp.variables['id'][:]

#close dataset
dataset.close()

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
# Cope with failing to create a region
# Only try to create regions that are within the echogram time period? Take care with 
#   regions that start before or end after the echogram time period.
# after region creation, set acoustic categories and labels.

for i, id in enumerate(region_id):
    region_mask = []
    dt = num2date(t[i], t_units, t_calendar) # convert timestamps to usable format
    for j, ping_time in enumerate(dt):
        region_mask.append({'time': ping_time.isoformat(timespec='milliseconds') + 'Z',
                            'depthRanges': [{'min': d[i][j*2].item(), 'max': d[i][j*2+1].item()}]})

    # and now send this region mask to LSSS    
    try:
        r = lsss.post('/lsss/module/PelagicEchogramModule/school-mask', json=region_mask)
        print('Created region ' + str(id) + ' as LSSS region ' + str(r['id'])) 
    except ValueError:
        print('Failed to create region ' + str(id))
        



    
    
        