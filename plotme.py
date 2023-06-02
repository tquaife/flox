import numpy as np
import matplotlib.pyplot as plt


class flox:

    def __init__(self, qepro_fn, flame_fn):
    
        self.qepro_fn=qepro_fn
        self.flame_fn=flame_fn
   
    def get_sample(self, sensor="qepro", sample=1, samp_type="VEG"):

        fp=open(self.qepro_fn)
        if sensor.lower() == "flame":
            fp=open(self.flame_fn)

        data=[]
        got_samp=False
        line=fp.readline()
        while line is not False:
            line_id=line.split(";")[0]
            if line_id==str(sample):
                 got_samp=True
            elif got_samp and line_id==samp_type:
                for datum in line.strip().strip(";").split(";")[1:]:
                    data.append(float(datum))                    
                break
            line=fp.readline()
            
        return np.array(data)
    
    def plot_sample(self, sensor="qepro", sample=1, samp_type="VEG"):
        
        data=self.get_sample(sensor, sample, samp_type)
    
        plt.plot(data)
        plt.show()


    def plot_veg_spectra(self, sample=1):
        
        sensor="flame"
        data_veg=self.get_sample(sensor, sample, samp_type="VEG")
        data_ref=self.get_sample(sensor, sample, samp_type="WR")
    
        plt.plot(data_veg/data_ref)
        plt.show()

    
if __name__=="__main__":    
    
    f=flox("data/120957.CSV","data/F120957.CSV")
    #f.plot_sample(sensor="flame", sample=1, samp_type="WR")    
    f.plot_veg_spectra( )
