import numpy as np
from datetime import datetime
from copy import copy

def print_header(lines):
    for item in lines[0].split(";"):
        print(item)

def get_var_col(varname,lines):
    for (i, item) in enumerate(lines[0].split(";")):
        item=item.strip("\"")
        if item.split()[0] == varname:
            return i
    return None

def get_var_units(varname,lines):
    for (i, item) in enumerate(lines[0].split(";")):
        item=item.strip("\"")
        if item.split()[0] == varname:
            return " ".join(item.split()[1:]).strip("[").strip("]")
    return None

def get_var_array(varname,lines):
    col=get_var_col(varname,lines)
    data=[]
    for line in lines[1:]:
        try:
            datum=float(line.split(";")[col])
        except:
            dataum=np.nan
        data.append(datum)
    return np.asarray(data)

def get_datetime_array(lines):
    col=get_var_col("datetime",lines)
    datearr=[]
    for line in lines[1:]:
        date=datetime.strptime(line.split(";")[col].split(".")[0], "%Y-%m-%d %H:%M:%S")
        datearr.append(date)
    return datearr

def filter_sif(data):
    data[data<-1.0]=np.nan
    data[data>3.0]=np.nan
    return data

def filter_data(data,lims=[0,1]):
    data[data<lims[0]]=np.nan
    data[data>lims[1]]=np.nan
    return data

def remove_dodgy_dates(lines):
    dates=get_datetime_array(lines)
    new_lines=[]
    new_lines.append(lines[0])
    for (i,line) in enumerate(lines[1:]):
        if dates[i] < datetime(2030,1,1):
            new_lines.append(line)
    return new_lines

def plot_sif(lines):
    units=get_var_units("SIF_A_ifld",lines)
    sif_a=get_var_array("SIF_A_ifld",lines)
    sif_a=filter_data(sif_a,lims=[-1.,3.])
    sif_b=get_var_array("SIF_B_ifld",lines)
    sif_b=filter_data(sif_b,lims=[-1.,3.])

    dt=get_datetime_array(lines)
    
    plt.plot(dt,sif_a,".",label="SIF a")
    plt.plot(dt,sif_b,".",label="SIF b")
    plt.xlabel("date")
    plt.legend()
    plt.ylabel("SIF "+units)
    plt.show()

def plot_vegindex(lines):
    dt=get_datetime_array(lines)

    ndvi=get_var_array("NDVI",lines)
    ndvi=filter_data(ndvi, lims=[0.7,1])
    evi=get_var_array("EVI",lines)
    evi=filter_data(evi, lims=[0.5,1])
    
    plt.plot(dt,ndvi,".",label="NDVI")
    plt.plot(dt,evi,".",label="EVI")
    plt.xlabel("date")
    plt.ylabel("VI")
    plt.legend()
    plt.show()


if __name__=="__main__":
    
    import matplotlib.pyplot as plt

    filename="ALL_INDEX_FLOX_2023-11-24_09_50_39.csv"
    
    with open(filename) as f:
        lines=f.readlines()
    lines=remove_dodgy_dates(lines)
    #print_header(lines)
    plot_sif(lines)    
    #plot_vegindex(lines)
    
