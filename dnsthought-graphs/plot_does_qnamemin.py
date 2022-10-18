import os.path
import time
from datetime import datetime, date, timedelta
import matplotlib
import sys
matplotlib.use('Agg')
import matplotlib.pyplot as pyplot
import matplotlib.pyplot as pp
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.dates as mpd
import pandas as pd

#matplotlib.style.use('seaborn-pastel')

OLD_TICKS = False
asns = pd.read_csv("asns.csv", sep=';')

def asn_label(asn):
    if asn == "Remaining":
        return asn
    return asns[asns["asn"]==asn]["name"].item()

def do_plot(dt_ts, data_ts, n_resolvers, labels):
    unknown_ts = [ row[0] - sum(row[1:])
            for row in zip(n_resolvers[len(n_resolvers)-len(dt_ts):], *data_ts)]

    fig, ax = pp.subplots()#figsize=(13, 7.3125))

    if len(dt_ts) > 270 and OLD_TICKS:
        ticks = []
        prev_month = dt_ts[0].month
        for day in dt_ts:
            if day.month != prev_month:
                ticks.append(day)
            prev_month = day.month

        ax.xaxis.set_ticks(ticks)
        ax.xaxis.set_major_formatter(mpd.DateFormatter('%Y-%m-%d'))
    elif len(dt_ts) > 120 and OLD_TICKS:
        ax.xaxis.set_major_formatter(mpd.DateFormatter('%Y-%m-%d'))

    ax.stackplot(dt_ts, data_ts + [unknown_ts], labels=labels)

    #ax.axvline(x=pd.to_datetime("2018-04-01"), color='black')
    #ax.axvline(x=pd.to_datetime("2020-01-01"), color='black')
    
    handles, labels = ax.get_legend_handles_labels()
    ax.set_xlim(dt_ts[0], dt_ts[-1])
    #ax.legend(handles[::-1], labels[::-1], ncol=1, loc='upper left')
    ax.legend(handles[::-1], labels[::-1], ncol=1, loc='upper center', bbox_to_anchor=(0.5, -0.2), prop={'size': 8})
    ax.set_ylabel('qmin-enabled probe resolvers')
    #fig.autofmt_xdate(rotation=45)

    # Tobias code
    pp.rcParams['lines.linewidth'] = 2
    pp.rcParams['font.size'] = 12
    pp.rcParams['xtick.labelsize'] = 12
    pp.rcParams['ytick.labelsize'] = 12
    pp.rcParams['legend.fontsize'] = 12
    pp.rcParams['axes.labelsize'] = 14
    pp.rcParams['axes.titlesize'] = 14

    pp.tight_layout()
    fig.set_size_inches(5,6)
    pp.savefig("dnsthought20221010asn.pdf", bbox_inches='tight')


    #pp.savefig("qnamemin-top10-resolver-ASNs-2022-05-24.svg", transparent=False, bbox_inches='tight')
    pp.close()
    

def plot_top(dt_ts, csv):
    offset = -1
    n_resolvers = csv['# resolvers'].values
    for i in range(len(n_resolvers)):
        if n_resolvers[i] != 0:
            offset = i
            break
    if offset < 0:
        return ''

    asn_totals = dict()
    # JM: wapped zip in lists because python3
    bands = [ list(zip( csv[f"resolver #{band} total"].values[offset:],
                    csv[f"resolver #{band} ASNs"].values[offset:]))
                for band in range(1,100) ]
    rem = csv['Remaining resolver ASNs count'].values[offset:]
    bands += [list(zip(rem, ['rem'] * len(rem)))]

    for band in bands:
        i = 0
        for total, ASNs in band:
            if n_resolvers[offset+i] == 0:
                i += 1
                continue
            if type(ASNs) is not str or not ASNs.startswith('AS'):
                i ++ 1
                continue
            ASNs = ASNs.split(',')
            for asn in ASNs:
                if asn not in asn_totals:
                    asn_totals[asn] = 0
                asn_totals[asn] += total / len(ASNs)
            i += 1

    top = sorted( [ (tot, asn) for asn, tot in asn_totals.items()
                    if asn != 'AS-1' ],
                reverse=True)
    size = 10
    labels = [asn for tot, asn in top][:size-1]
    labels += ['Remaining']
    
    data_ts = list()
    i = 0
    for row in zip(*bands):
        if n_resolvers[offset+i] == 0:
            i += 1
            data_ts.append([0] * size)
            continue
        asn_dict = {}
        top_row = list()
        rem = 0
        for total, ASNs in row:
            if type(ASNs) is not str:
                continue
            if not ASNs.startswith('AS'):
                rem += total
                continue
            ASNs = ASNs.split(',')
            for asn in ASNs:
                asn_dict[asn] = total / len(ASNs)
        for j in range(len(labels)-1):
            asn = labels[j]
            top_row.append(asn_dict.get(asn, 0))
            asn_dict[asn] = 0
        top_row.append(sum(asn_dict.values()) + rem)
        data_ts.append(top_row)
        i += 1

    data_ts = [list(ts) for ts in zip(*data_ts)]
    labels = [asn_label(asn) for asn in labels]
    do_plot(dt_ts[offset:], data_ts, n_resolvers, labels)


csv = pd.read_csv("does_qnamemin_2022-10-10.csv", low_memory=False)
#ts_series = [ datetime.strptime(iso_dt, '%Y-%m-%dT%H:%M:%SZ')
#        for iso_dt in csv['datetime'].values ]
ts_series = list(pd.to_datetime(csv["datetime"]))
plot_top(ts_series, csv)

