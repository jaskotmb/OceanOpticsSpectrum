import sys
sys.path.append('C:\\Users\\Jerry\\IdeaProjects\\OLED_Tools')
import OLEDTools
import os
import glob

#files = []
os.chdir("C:\\Users\\Jerry\\IdeaProjects\\OceanOpticsSpectrum")

filesC50 = ["190719M71Vfr_2.csv","190719M75Vfr_1.csv"]
filesC25 = ["190730M13Vfr_5.csv","190730M13Vfr_8.csv","190730M13Vf_3.csv"]
filesH50 = ["190718M72Vfr_1.csv","190718M72Vfr_3.csv","190718M73Vfr_1.csv","190718M74Vfr_3.csv"]
files = filesC50 + filesC25 + filesH50 + ["190719M24Vt_fr_1.csv"]
files = ["190719M24Vfr_1.csv"]

print(files)
cols = ["black","red","blue","orange","brown"]
cols = ["purple"]*len(filesC50)+["blue"]*len(filesC25)+["red"]*len(filesH50)+["green"]

OLEDTools.multipleQuenchPlot("V",files,cols,"V")
#OLEDTools.quenchAnalyzePL(files[0],2)`
