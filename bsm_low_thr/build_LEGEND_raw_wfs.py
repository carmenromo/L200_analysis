import sys
import argparse

from daq2lh5 import build_raw
from parse   import parse

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('period'       , type = int,                                help = "LEGEND data period"   )
    parser.add_argument('run'          , type = int,                                help = "LEGEND run number"    )
    parser.add_argument('data_type'    , type = str,                                help = "Data type: tst or cal")
    parser.add_argument('in_dir'       , type = str,                                help = "Input files path"     )
    parser.add_argument('filename'     , type = str,                                help = "Name of input files"  )
    parser.add_argument('out_dir'      , type = str,                                help = "Output files path"    )
    parser.add_argument('ifiles_format', type = str, default = "orca",              help = "Input files format"   )
    parser.add_argument('json_file'    , type = str, default = "2ge_all_spms.json", help = "Json file"            )
    return parser.parse_args()

arguments     = pf.parse_args(sys.argv)
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
    break

print(run, in_dir, out_dir)

f_parse  = parse(file_format, filename)
#if not f_parse: continue
out_file = out_dir + 'raw_wf_' + f_parse['datetime'] + '.lh5'

build_raw(in_file,
	      in_stream_type=in_stream_type,
	      out_spec      =json_file,
	      out           =out_file,
	      overwrite     =True)