import os
import sys

from daq2lh5 import build_raw
from parse   import parse

period    = sys.argv[1]
run       = sys.argv[2]
data_type = sys.argv[3]	#tst                                                                                                                                

f_format = "{key}.orca.gz"

file_format = "l200-{period}-{run}-{data_type}-{datetime}.orca.gz"

in_dir  = f"/global/cfs/cdirs/m2676/data/lngs/l200/orca_data/Data/p0{period}/r00{run}/"
out_dir = f"/pscratch/sd/r/romo/legend_data/l200/tier/raw/{data_type}/p0{period}/r00{run}/"

print(run, in_dir, out_dir)
it = os.scandir(in_dir)
for i,entry in enumerate(it):
    # if i != 2: continue                                                                                                                                   
    in_file = in_dir + entry.name
    f_parse = parse(f_format,entry.name)

    if not f_parse: continue
    key = f_parse['key']
    out_file = out_dir + key  + '.lh5'

    if not parse(file_format,entry.name): continue

    build_raw(in_file,
	      in_stream_type="ORCA",
	      out_spec="2ge_all_spms.json",
	      out=out_file,
	      overwrite=True)