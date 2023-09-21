import sys

from parse_functions import parse_args

from daq2lh5 import build_raw
from parse   import parse

arguments     = parse_args(sys.argv)
period        = arguments.period
run           = arguments.run
data_type     = arguments.data_type
in_dir        = arguments.in_dir
filename      = arguments.filename
out_dir       = arguments.out_dir
ifiles_format = arguments.ifiles_format
json_file     = arguments.json_file

if ifiles_format=="orca":
    file_format    = "l200-{period}-{run}-{data_type}-{datetime}.orca.gz"
    in_stream_type = "ORCA"
elif ifiles_format=="fcio":
    file_format    = "l200-{period}-{run}-{data_type}-{datetime}_FCIO_0.fcio"
    in_stream_type = "FlashCam"
else:
    print(f"Input files format {ifiles_format} not recognized!")

print(run, in_dir, out_dir)

f_parse  = parse(file_format, filename)
#if not f_parse: continue
in_file  = in_dir + filename
out_file = out_dir + 'raw_wf_' + f_parse['datetime'] + '.lh5'

build_raw(in_file,
	      in_stream_type=in_stream_type,
	      out_spec      =json_file,
	      out           =out_file,
	      overwrite     =True)