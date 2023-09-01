import os
import sys

from daq2lh5 import build_raw
from parse   import parse

period    = sys.argv[1]
run       = sys.argv[2]
data_type = sys.argv[3]	#tst
in_dir    = sys.argv[4]
filename  = sys.argv[5]
out_dir   = sys.argv[6]

file_format = "l200-{period}-{run}-{data_type}-{datetime}.orca.gz"

print(run, in_dir, out_dir)

f_parse  = parse(file_format, filename)
#if not f_parse: continue
out_file = out_dir + 'raw_wf_' + f_parse['datetime']  + '.lh5'

build_raw(in_file,
	      in_stream_type="ORCA",
	      out_spec="2ge_all_spms.json",
	      out=out_file,
	      overwrite=True)