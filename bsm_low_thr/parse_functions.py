import argparse

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