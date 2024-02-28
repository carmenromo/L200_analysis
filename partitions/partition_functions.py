import re
import numpy as np

import matplotlib.pyplot as plt

from datetime import datetime, timezone

from itertools import cycle


type_mapping = {"V0": "ICPC", "B0": "BEGe", "C0": "Coax", "P0": "PPC"}
det_colors = ['#BFC2C7', '#07A9FF', '#FF9E21', '#1A2A5B']

def cal_energy(e_uncal, cal_pars):
    """ Function to calibrate energy """
    if len(cal_pars.keys())==2:
        return cal_pars['a'] * e_uncal + cal_pars['b'], 'lin'
    elif len(cal_pars.keys())==3:
        return cal_pars['a'] * e_uncal **2 + cal_pars['b'] * e_uncal + cal_pars['c'], 'quad'

def uncal_quad(FWHM_keV, cal_pars):
    """ Quadratic function to go back to ADC from keV """
    FWHM_adc = (-cal_pars['b']+np.sqrt(cal_pars['b']**2-2*cal_pars['a']*(cal_pars['c']-FWHM_keV)))/(2*cal_pars['a'])
    return FWHM_adc

def uncal_lin(FWHM_keV, cal_pars):
    """ Linear function to go back to ADC from keV """
    #FWHM_adc = (FWHM_keV - cal_pars['c'])/cal_pars['b']
    FWHM_adc = FWHM_keV/cal_pars['b']
    return FWHM_adc

def poly(x, pars):
    """
    A polynomial function with pars following the polyfit convention
    """
    result = x*0 # do x*0 to keep shape of x (scalar or array)
    if len(pars) == 0: return result
    result += pars[-1]
    for i in range(1, len(pars)):
        result += pars[-i-1]*x
        x = x*x
    return result

def uncal_poly(FWHM_keV, pars):
    derco = np.polyder(np.poly1d(pars)).coefficients
    der   = poly(FWHM_keV, derco)
    return FWHM_keV / der


def get_ch_name(ch_rawid: int, ge_all, ge_rawid):
    """ Returns the channel name of the detector from the rawid """
    return ge_all[np.where((np.array(ge_rawid)==ch_rawid))[0][0]]

def get_ch_rawid(ch_name: str, ge_all, ge_rawid):
    """ Returns the rawid of the detector from the channel name """
    return ge_rawid[np.where((np.array(ge_all)==ch_name))[0][0]]

def get_det_type(ch_name: str):
    """ Returns the detector type from the channel name """
    for prefix, det_type in type_mapping.items():
        if prefix in ch_name:
            return det_type
        
def get_timestamp_from_filename(filename):
    """ Returns the timestamp of the file from the filename """
    timestamp  = re.compile(r'\d{8}T\d{6}Z').search(filename)
    return datetime.strptime(timestamp.group(), '%Y%m%dT%H%M%SZ').replace(tzinfo=timezone.utc)


def plot_variable_for_det_type(all_params_ch, det_list, ge_all, ge_rawid, var='Qbb_fwhms_in_keV', var_err='Qbb_fwhms_err_in_keV', var_name='FWHM Qbb (keV)', errs=True, ylims=(1.5, 6), title='E res'):

    fig, axs = plt.subplots(2, 2, figsize=(13.5, 10))
    for ax, d_type, col in zip(axs.flatten(), type_mapping.values(), det_colors):
        for channel in det_list:
            det_type = get_det_type(get_ch_name(int(channel[2:]), ge_all, ge_rawid))
            if det_type==d_type:
                var_keys = list(all_params_ch[channel][var]    .keys())
                var_vals = list(all_params_ch[channel][var]    .values())
                if errs:
                    var_errs = list(all_params_ch[channel][var_err].values())
                    ax.errorbar(var_keys, var_vals, yerr=var_errs,
                         marker='*', linestyle='--', markersize=6, label=channel, color=col, linewidth=0.8)
                else:
                    ax.errorbar(var_keys, var_vals,
                         marker='*', linestyle='--', markersize=6, label=channel, color=col, linewidth=0.8)
                
                ax.tick_params(axis='x', labelsize=13, rotation=90)
                ax.tick_params(axis='y', labelsize=13)
                ax.set_title(f'{d_type}', fontsize=15)
                ax.set_ylabel(f'{var_name}', fontsize=15)
                ax.set_ylim(ylims)
    fig.suptitle(f'{title}', fontsize=18)
    plt.tight_layout()
    plt.show()


def compute_partitions_poly(all_params_ch, channel, peak, col='teal', ylim='', mean_part=True, divide_sigma_by=1):
    mus    = list(all_params_ch[channel]['mus_peaks'][peak].values())
    sigmas = np.array(list(all_params_ch[channel]['Qbb_fwhms_in_ADC_poly'].values()))/2.355
    
    partition_change = [0]
    
    if mean_part:
        start_mu = []
        for i,(mu,sig) in enumerate(zip(mus, sigmas)):
            if i==0:
                start_mu.append(mu)
            else:
                if np.abs(mu - np.mean(start_mu)) > (np.abs(sig))/divide_sigma_by:
                    partition_change.append(i)
                    start_mu = [mu]
                else:
                    start_mu.append(mu)
                        
    else:
        start_mu = 0
        for i,(mu,sig) in enumerate(zip(mus, sigmas)):
            if i==0:
                start_mu = mu
            else:
                if np.abs(mu - start_mu) > (np.abs(sig))/divide_sigma_by:
                    partition_change.append(i)
                start_mu = mu
    
    partition_change.append(len(mus)-1)
    
    return partition_change


def plot_mus_and_partitions(all_params_ch, psd_status, usability, list_channels, peak, ge_all, ge_rawid, ncol=3, figsize=(13.5, 25), mean_part=True, divide_sigma_by=1):
    _, axs = plt.subplots(int(np.ceil(len(list_channels)/ncol)), ncol, figsize=figsize)
    for ax, channel in zip(axs.flatten(), list_channels):
        try:
            keys    = list(all_params_ch[channel]['mus_peaks']    [peak].keys())
            mus     = list(all_params_ch[channel]['mus_peaks']    [peak].values())
            mus_err = list(all_params_ch[channel]['mus_err_peaks'][peak].values())
            
            psd_stat = np.unique(list(psd_status[channel].values()))
            usab     = np.unique(list(usability [channel].values()))
            
            partition_change = compute_partitions_poly(all_params_ch, channel, peak, mean_part=mean_part,
                                                       divide_sigma_by=divide_sigma_by)
            det_name = get_ch_name(int(channel[2:]), ge_all, ge_rawid)
            det_type = get_det_type(det_name)
    
            ax.errorbar(keys, mus, yerr=mus_err, marker='*', linestyle='--', markersize=8, label=det_type)
    
            for i,col in zip(range(len(partition_change)-1), cycle(['teal', 'grey', 'orange', 'indianred'])):
                ax.axvspan(keys[partition_change[i]], keys[partition_change[i+1]], alpha=0.2, color=col)
    
            ax.tick_params(axis='x', labelsize=8, rotation=90)
            ax.tick_params(axis='y', labelsize=10)
            ax.set_title(f'{det_type}, ({det_name}), {psd_stat}, {usab}', fontsize=11)
            ax.set_ylabel('Mu position (ADC)', fontsize=10)
            
            ax.set_ylim(np.min(mus)-5, np.max(mus)+5)
        except KeyError:
            continue
        
    plt.tight_layout()    
    plt.show()


