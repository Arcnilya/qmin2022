import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime
import sys

if len(sys.argv) < 2:
    exit("Missing argument")

data = pd.read_csv(sys.argv[1], low_memory=False)
interesting_cols = ["datetime", 
                    "# probes", 
                    "# resolvers", 
                    "does_qnamemin", 
                    "doesnt_qnamemin", 
                    "does_qnamemin_prbs", 
                    "doesnt_qnamemin_prbs"]
#print(data[interesting_cols])

data["answering"] = data["does_qnamemin"] + data["doesnt_qnamemin"]
data["qmin_share"] = data["does_qnamemin"] / data["answering"]

#matplotlib.style.use('seaborn-pastel')
fig, ax = plt.subplots()#figsize=(13, 7.3125))

ax.plot(pd.to_datetime(data["datetime"]), data["qmin_share"])

# Cloudflare enabled qmin by default
#ax.axvline(x=pd.to_datetime("2018-04-01"), color='black')
# Resolvers in Google ASN enabling qmin
#ax.axvline(x=pd.to_datetime("2020-01-01"), color='black')

ax.set_ylabel('qmin share')
ax.set_ylim(0,1)

# Tobias code
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['font.size'] = 12
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['legend.fontsize'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 14
plt.tight_layout()
fig.set_size_inches(5,3)
plt.savefig("dnsthought20221010share.pdf", bbox_inches='tight')


#plt.legend(loc='upper left')
#plt.savefig(f"{sys.argv[1].split('.')[0]}_share.svg", transparent=False, bbox_inches='tight')
#plt.show()
