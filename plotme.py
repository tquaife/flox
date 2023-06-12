import sys

import numpy as np
import matplotlib.pyplot as plt

class flox_data:

    def __init__(self, qepro_fn, flame_fn, calib_fn):
        """Class to read and process FloX data
        Currently only handles the linear calibration files
        """
    
        self.qepro_fn=qepro_fn
        self.flame_fn=flame_fn
        self.calib_fn=calib_fn
        
        self.read_calibration_file( )
        
        #some testing of my understanding, **delete**
        #(note: this is the right equation as matches 
        #calibration file, but better just to read file!)
        x=np.arange(1024)*2
        self.flame_wl_test=340.17858887+x*0.3839645982+x*x*-2.25897e-005+x*x*x*-8.94138e-010
   
    def read_calibration_file(self):
        
        self.qepro_wl=[]
        self.qepro_up_coef=[]
        self.qepro_dn_coef=[]
        self.flame_wl=[]
        self.flame_up_coef=[]
        self.flame_dn_coef=[]

        with open(self.calib_fn) as fp:        
            #read first line to skip header
            line=fp.readline()
            #read first line of data
            line=fp.readline()
            while line is not "":
                self.qepro_wl.append(float(line.split(";")[0]))
                self.qepro_up_coef.append(float(line.split(";")[1]))
                self.qepro_dn_coef.append(float(line.split(";")[2]))
                self.flame_wl.append(float(line.split(";")[3]))
                self.flame_up_coef.append(float(line.split(";")[4]))
                self.flame_dn_coef.append(float(line.split(";")[5]))
                #read next line of data
                line=fp.readline().strip()
         
        self.qepro_wl=np.asarray(self.qepro_wl)
        self.qepro_up_coef=np.asarray(self.qepro_up_coef)
        self.qepro_dn_coef=np.asarray(self.qepro_dn_coef)
        self.flame_wl=np.asarray(self.flame_wl)
        self.flame_up_coef=np.asarray(self.flame_up_coef)
        self.flame_dn_coef=np.asarray(self.flame_dn_coef)

   
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

        #apply calibration
        if sensor.lower() == "flame" and ( samp_type == "VEG" or samp_type == "DC_VEG"):
            coef=self.flame_dn_coef
        elif sensor.lower() == "flame" and ( samp_type == "WR" or samp_type == "DC_WR"):
            coef=self.flame_up_coef
        elif sensor.lower() == "qepro" and ( samp_type == "VEG" or samp_type == "DC_VEG"):
            coef=self.qepro_dn_coef
        elif sensor.lower() == "qepro" and ( samp_type == "WR" or samp_type == "DC_WR"):
            coef=self.qepro_up_coef
            
        return np.array(data)*coef


    def get_avg_sample(self, sensor="qepro", samples=[1,2,3], samp_type="VEG"):
        data=None
        for i in samples:
            if data is None:
                data=self.get_sample(sensor=sensor, sample=i, samp_type=samp_type)
            else:
                data+=self.get_sample(sensor=sensor, sample=i, samp_type=samp_type)
        return data/float(len(samples))


    
def plot_qepro_spectra(flox_data,  samples=[1,]):
    
    sensor="qepro"
    data_veg=flox_data.get_avg_sample(sensor, samples, samp_type="VEG")
    data_ref=flox_data.get_avg_sample(sensor, samples, samp_type="WR")
    data_veg_dc=flox_data.get_avg_sample(sensor, samples, samp_type="DC_VEG")
    data_ref_dc=flox_data.get_avg_sample(sensor, samples, samp_type="DC_WR")

    radiance_spectra_dn=(data_veg-data_veg_dc)
    radiance_spectra_up=(data_ref-data_ref_dc)
    #refl=radiance_spectra_dn/radiance_spectra_up
    
    plt.plot(flox_data.qepro_wl,radiance_spectra_dn)
    plt.plot(flox_data.qepro_wl,radiance_spectra_up)
    plt.ylabel("Radiance (W/m2/sr/nm)")

    #plt.plot(flox_data.qepro_wl,refl)
    
    plt.xlabel("Wavelength (nm)")
    plt.xlim([650,800])
    #plt.ylim([0,0.5])
    plt.show()



def plot_veg_spectra(flox_data, samples=[1,]):
    
    model=np.genfromtxt("modelled_spectra.txt")
    #print(model[:,0])
    
    sensor="flame"
    data_veg=flox_data.get_avg_sample(sensor, samples, samp_type="VEG")
    data_ref=flox_data.get_avg_sample(sensor, samples, samp_type="WR")
    data_veg_dc=flox_data.get_avg_sample(sensor, samples, samp_type="DC_VEG")
    data_ref_dc=flox_data.get_avg_sample(sensor, samples, samp_type="DC_WR")

    refl_spectra=(data_veg-data_veg_dc)/(data_ref-data_ref_dc)/(np.pi*2)


    sensor="qepro"
    data_veg=flox_data.get_avg_sample(sensor, samples, samp_type="VEG")
    data_ref=flox_data.get_avg_sample(sensor, samples, samp_type="WR")
    data_veg_dc=flox_data.get_avg_sample(sensor, samples, samp_type="DC_VEG")
    data_ref_dc=flox_data.get_avg_sample(sensor, samples, samp_type="DC_WR")
    radiance_spectra_dn=(data_veg-data_veg_dc)
    radiance_spectra_up=(data_ref-data_ref_dc)
    refl_spectra_qepro=radiance_spectra_dn/radiance_spectra_up
    qe_chop=10

    plt.plot(flox_data.flame_wl,refl_spectra,linewidth=3)
    plt.plot(flox_data.flame_wl_test,refl_spectra)
    plt.plot(flox_data.qepro_wl[qe_chop:],refl_spectra_qepro[qe_chop:])
    #plt.plot(model[:,0],model[:,1])
    plt.ylim([0,0.5])
    plt.xlim([400,900])
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("BRF (-)")
    plt.show()

    
if __name__=="__main__":    
    
    f=flox_data("data/FLOX__230609/142937.CSV","data/FLOX__230609/F142937.CSV","CAL_FLOX_JB-030-TQ_2019-12-19.csv")
    #plot_veg_spectra(f, samples=[15,16,17,18,19,20,21,22,23] )
    plot_qepro_spectra(f, samples=[15,16,17,18,19,20,21,22,23] )
    
    
    
