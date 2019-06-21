import sys
sys.path.append('C:\\Users\\jasko\\IdeaProjects\\OLED_Tools')
import OLEDTools
import os
import glob

#files = []
os.chdir("C:\\Users\\jasko\\IdeaProjects\\OceanOpticsSpectrum")
#for file in glob.glob("*.csv"):
#    files.append(file)
num = 4
iterations = 4
files = ["190613M1{0}_1.csv".format(num)]
for i in range(2,iterations+1):
    print(i)
    fileTemp = "190606M1{0}_{1}.csv".format(num,i)
    files.append(fileTemp)
print(files)

filesRT=["190605M12_4.csv","190605M13_3.csv","190605M27_4.csv","190605M28_4.csv","190605M33_4.csv","190605M38_1.csv",
         "190605M37_4.csv","190605M36_3.csv","190605M35_3.csv"]
filesc50=["190606M12_5.csv","190606M13_4.csv"]
filesh50=["190605M73_5.csv","190605M74_4.csv","190605M77_4.csv"]
filesh0=["190613M12_1.csv"]
#files=filesRT+filesc50+filesh50+filesh0
cols=["black"]*9+["blue"]*2+["red"]*3+["green"]*1
#cols = ["black"]*1+["red"]*1+["blue"]*1+["orange","brown","black","purple"]*5
OLEDTools.multipleQuenchPlot(files,cols)
#OLEDTools.quenchAnalyzePL(files[0],2)`
