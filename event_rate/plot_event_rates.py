
from legend_plot_style import LEGENDPlotStyle as lps
lps.use('legend_talks')

import os
import sys
import glob
import pandas as pd
import numpy  as np

import matplotlib.pyplot    as plt
import event_rate_functions as erf

from datetime import datetime


SKIM_DIR = sys.argv[1]

data       = erf.read_and_concat_data(SKIM_DIR)
data.index = pd.to_datetime(data.index, unit='s') ## Express timestamps in seconds
data_filt  = erf.data_selection(data)

runs_start_lines, runs_end_lines = [], []

for filename in np.sort(glob.glob(SKIM_DIR + '/*/*hdf')):
    df_filename    = pd.read_hdf(filename)
    irun_t, frun_t = pd.to_datetime(df_filename.index[[0, -1]], unit='s')
    runs_start_lines.append(irun_t)
    runs_end_lines  .append(frun_t)

runs_start_lines = np.array(runs_start_lines)
runs_end_lines   = np.array(runs_end_lines)


midpoint_labels = [f'p03-r{i:03d}' for i in range(6)] + [f'p04-r{i:03d}' for i in range(4)]
midpoints       = [start + (end - start) / 2 for start, end in zip(runs_start_lines, runs_end_lines)]

colors  = ['legend_gold', 'yellow']
labs    = ['After QC',    'After QC + LAr veto']
vals    = [True,          False]

fig, ax = plt.subplots(figsize=(10, 6))
for val, col, lab in zip(vals, colors, labs):
    data_cut_gold          = data_filt[(data_filt.is_usable_aoe==True)&(data_filt.is_lar_rejected==val)]
    data_cut_gold_series   = erf.resample_df(data_cut_gold, '1H')
    ax.plot(data_cut_gold_series.index, data_cut_gold_series, linewidth=0.8, color=lps.colors[col], alpha=0.8, label=f'{lab}')

ax.set_legend_logo(position='upper right', logo_type = 'preliminary')
ax.set_title('Golden dataset')
ax.set_ylabel('Event Rate (mHz)')
leg = fig.legend(ncol=1, loc='upper left', bbox_to_anchor=(0.09, 0.92))
for line in leg.get_lines():
    line.set_linewidth(2)

ax.set_xticks(midpoints)
ax.set_xticklabels(midpoint_labels, rotation=45)
ax.set_ylim(-5, 130)
plt.savefig("event_rates_golden_LAr.png", bbox_inches='tight')
