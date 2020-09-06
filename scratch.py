import sys
sys.path.append('C:\\Users\\Jerry\\IdeaProjects\\OLED_Tools')
import OLEDTools
import os
import glob

#files = []
os.chdir("C:\\Users\\Jerry\\IdeaProjects\\OceanOpticsSpectrum")
mCBPTC50L = ["200108M11Vpbr_1.csv","200108M13Vpbr_1.csv","200108M12Vpbr_1.csv"]
mCBPTC50 = ["200108M11Vpbr_1.csv","200108M13Vpbr_1.csv","200108M12Vpbr_1.csv"]
mCBPTC25L = ["191214M13Vpbr_1.csv","191214M26Vpbr_1.csv","191214M34Vpbr_1.csv","191214M38Vpbr_1.csv",
             "191214M36Vpbr_1.csv","191214M22Vpbr_1.csv","191214M32Vpbr_1.csv"]
mCBPTC25 = ["191214M11Vpbr_1.csv","191214M14Vpbr_1.csv","191214M18Vpbr_1.csv","191214M21Vpbr_1.csv",
            "191214M24Vpbr_1.csv","191214M27Vpbr_1.csv","191214M31Vpbr_1.csv","191214M15Vpbr_2.csv",
            "191214M25Vpbr_1.csv","191214M35Vpbr_1.csv"]
mCBPTC00 = ["200109M11Vpbr_1.csv","200109M18Vpbr_1.csv","200109M21Vpbr_1.csv","200109M28Vpbr_1.csv",
            "200109M27Vpbr_1.csv"]
mCBPTC00L = ["200109M12Vpbr_1.csv"]
mCBPTH25 = ["191209M13Vpbr_1.csv","191209M14Vpbr_1.csv","191209M28Vpbr_1.csv","191209M27Vpbr_1.csv",
             "191209M26Vpbr_1.csv","191209M36Vpbr_1.csv","191209M44Vpbr_1.csv","191209M47Vpbr_1.csv",
             "191209M58Vpbr_1.csv","191209M61Vpbr_1.csv","191209M67Vpbr_1.csv","191209M22Vpbr_1.csv",
            "191209M25Vpbr_1.csv","191209M32Vpbr_1.csv"]
mCBPTH25L = ["191209M18Vpbr_1.csv","191209M17Vpbr_1.csv","191209M16Vpbr_1.csv","191209M11Vpbr_1.csv",
             "191209M21Vpbr_1.csv","191209M23Vpbr_1.csv","191209M24Vpbr_1.csv","191209M31Vpbr_1.csv",
             "191209M33Vpbr_1.csv","191209M38Vpbr_1.csv","191209M41Vpbr_1.csv","191209M43Vpbr_1.csv",
             "191209M48Vpbr_1.csv","191209M46Vpbr_1.csv","191209M54Vpbr_1.csv","191209M51Vpbr_1.csv",
             "191209M53Vpbr_1.csv","191209M57Vpbr_1.csv","191209M63Vpbr_1.csv","191209M64Vpbr_1.csv",
             "191209M68Vpbr_1.csv","191209M35Vpbr_1.csv","191209M45Vpbr_1.csv","191209M42Vpbr_2.csv",
             "191209M66Vpbr_1.csv"]
mCBPTH50 = ["200107M13Vpbr_1.csv","200107M17Vpbr_1.csv","200107M23Vpbr_1.csv","200107M24Vpbr_1.csv",
            "200107M28Vpbr_2.csv","200107M31Vpbr_1.csv","200107M33Vpbr_1.csv"]
mCBPTH50L = ["200107M27Vpbr_1.csv","200107M26Vpbr_1.csv","200107M38Vpbr_1.csv",
             "200107M37Vpbr_1.csv"]
mx10 = ["200114M13Vpbr_1.csv","200114M14Vpbr_1.csv","200114M18Vpbr_1.csv","200114M17Vpbr_1.csv",
        "200114M15Vpbr_1.csv","200114M12Vpbr_1.csv","200114M15Vpbr_1.csv","200114M16Vpbr_1.csv"]

mCBPfilesA = mCBPTC50L+mCBPTC50+mCBPTC25L+mCBPTC25+mCBPTC00L+mCBPTC00+mCBPTH25L+mCBPTH25+mCBPTH50L+mCBPTH50
mCBPcolsA = ["blue"]*(len(mCBPTC50L)+len(mCBPTC50))+["deepskyblue"]*(len(mCBPTC25L)+len(mCBPTC25))+\
            ["grey"]*(len(mCBPTC00L)+len(mCBPTC00))+["darkorange"]*(len(mCBPTH25L)+len(mCBPTH25))+\
            ["red"]*(len(mCBPTH50L)+len(mCBPTH50))
colsA=mCBPcolsA+["black","green","black","red","brown","yellow"]
filesA=mCBPfilesA+["200221M27Vpbr_1.csv"]#,"200123M21Vpbr_1.csv"]

mCBPfilesL = mCBPTC50L+mCBPTC25L+mCBPTC00L+mCBPTH25L+mCBPTH50L
mCBPcolsL = ["blue"]*len(mCBPTC50L)+["dodgerblue"]*len(mCBPTC25L)+["grey"]*len(mCBPTC00L)\
           +["orange"]*len(mCBPTH25L)+["red"]*len(mCBPTH50L)
#cols=mCBPcolsL+["green","black","purple","brown","yellow"]
#files=mCBPfilesL+["200503M18Vpbr_1.csv","200503M18Vpfr_1.csv","200503M17Vpfr_1.csv","200503M17Vpbr_1.csv"]

BSBfilesF = ["200503M12Vpfr_1.csv","200503M16Vpfr_1.csv","200503M15Vpfr_1.csv","200503M23Vpfr_1.csv",
             "200503M24Vpfr_1.csv","200503M28Vpfr_1.csv","200503M27Vpfr_1.csv","200503M22Vpfr_1.csv",
             "200503M25Vpfr_1.csv","200503M26Vpfr_1.csv"]
BSBfilesB = ["200503M12Vpbr_1.csv","200503M16Vpbr_1.csv","200503M15Vpbr_1.csv","200503M23Vpbr_1.csv",
             "200503M24Vpbr_1.csv","200503M28Vpbr_1.csv","200503M27Vpbr_1.csv","200503M22Vpbr_1.csv",
             "200503M25Vpbr_1.csv"]
BSBfilesF0 = ["200505M11Vpfr_1.csv","200505M14Vpfr_1.csv","200505M18Vpfr_1.csv","200505M17Vpfr_1.csv",
              "200505M12Vpfr_1.csv","200505M16Vpfr_1.csv","200505M15Vpfr_1.csv","200505M21Vpfr_1.csv",
              "200505M23Vpfr_1.csv","200505M24Vpfr_1.csv","200505M28Vpfr_1.csv","200505M27Vpfr_1.csv",
              "200505M22Vpfr_1.csv","200505M26Vpfr_1.csv"]
BSBfilesB0 = ["200505M11Vpbr_1.csv","200505M14Vpbr_1.csv","200505M18Vpbr_1.csv","200505M17Vpbr_1.csv",
              "200505M12Vpbr_1.csv","200505M16Vpbr_1.csv","200505M15Vpbr_1.csv","200505M21Vpbr_1.csv",
              "200505M23Vpbr_1.csv","200505M24Vpbr_1.csv","200505M22Vpbr_1.csv","200505M26Vpbr_1.csv"]
BSBfilesF30 = ["200505M41Vpfr_1.csv","200505M44Vpfr_1.csv","200505M48Vpfr_1.csv","200505M47Vpfr_1.csv",
               "200505M42Vpfr_1.csv","200505M45Vpfr_1.csv","200505M54Vpfr_1.csv","200505M58Vpfr_1.csv",
                "200505M57Vpfr_1.csv","200505M52Vpfr_1.csv","200505M56Vpfr_1.csv"]
BSBfilesB30 = ["200505M41Vpbr_1.csv","200505M44Vpbr_1.csv","200505M48Vpbr_1.csv","200505M47Vpbr_1.csv",
               "200505M42Vpbr_1.csv","200505M45Vpbr_1.csv","200505M54Vpbr_1.csv","200505M58Vpbr_1.csv",
               "200505M57Vpbr_1.csv","200505M52Vpbr_1.csv","200505M56Vpbr_1.csv"]
BSBfilesF100 = ["200521M11Vpfr_1.csv","200521M12Vpfr_1.csv","200521M13Vpfr_1.csv","200521M14Vpfr_1.csv",
                "200521M15Vpfr_1.csv","200521M16Vpfr_1.csv","200521M17Vpfr_1.csv"]
BSBfilesF50 = ["200526M11Vpfr_1.csv","200526M12Vpfr_1.csv","200526M14Vpfr_1.csv","200526M15Vpfr_1.csv",
                 "200526M16Vpfr_1.csv","200526M18Vpfr_1.csv"]

MxFilesB00 = ["191209M13Vpbr_1.csv","191209M14Vpbr_1.csv","191209M16Vpbr_1.csv","191209M17Vpbr_1.csv","191209M18Vpbr_1.csv",
              "191209M21Vpbr_1.csv","191209M22Vpbr_1.csv","191209M23Vpbr_1.csv","191209M24Vpbr_1.csv","191209M25Vpbr_1.csv",
              "191209M26Vpbr_1.csv","191209M27Vpbr_1.csv","191209M28Vpbr_1.csv","191209M31Vpbr_1.csv","191209M32Vpbr_1.csv",
              "191209M33Vpbr_1.csv","191209M35Vpbr_1.csv","191209M36Vpbr_1.csv","191209M37Vpbr_1.csv","191209M38Vpbr_1.csv",
              "191209M41Vpbr_1.csv","191209M43Vpbr_1.csv","191209M44Vpbr_1.csv","191209M45Vpbr_1.csv","191209M46Vpbr_1.csv",
              "191209M47Vpbr_1.csv","191209M48Vpbr_1.csv","191209M51Vpbr_1.csv","191209M52Vpbr_1.csv","191209M53Vpbr_1.csv",
              "191209M55Vpbr_1.csv","191209M57Vpbr_1.csv","191209M58Vpbr_1.csv","191209M62Vpbr_1.csv","191209M63Vpbr_1.csv",
              "191209M64Vpbr_1.csv","191209M66Vpbr_1.csv","191209M67Vpbr_1.csv","191209M68Vpbr_1.csv"]
MxFilesB00_2 = ["200221M12Vpbr_1.csv","200221M15Vpbr_1.csv","200221M16Vpbr_1.csv","200221M21Vpbr_1.csv","200221M23Vpbr_1.csv",
                "200221M24Vpbr_1.csv","200221M25Vpbr_1.csv","200221M26Vpbr_1.csv","200221M27Vpbr_1.csv","200221M31Vpbr_1.csv",
                "200221M32Vpbr_1.csv","200221M33Vpbr_1.csv","200221M34Vpbr_1.csv","200221M35Vpbr_1.csv","200221M36Vpbr_1.csv"]
MxFilesB10 = ["200623M11Vpbr_1.csv","200623M13Vpbr_1.csv","200623M14Vpbr_1.csv","200623M18Vpbr_1.csv","200623M17Vpbr_1.csv",
              "200623M12Vpbr_1.csv","200623M15Vpbr_1.csv","200623M16Vpbr_1.csv","200623M21Vpbr_1.csv","200623M23Vpbr_1.csv",
              "200623M24Vpbr_1.csv","200623M27Vpbr_1.csv","200623M22Vpbr_1.csv","200623M25Vpbr_1.csv","200623M26Vpbr_1.csv",
              "200623M31Vpbr_1.csv","200623M33Vpbr_1.csv","200623M37Vpbr_1.csv","200623M32Vpbr_1.csv","200623M35Vpbr_1.csv",
              "200623M36Vpbr_1.csv"]
MxFilesB20 = ["200224M11Vpbr_1.csv","200224M12Vpbr_1.csv","200224M13Vpbr_1.csv","200224M14Vpbr_1.csv","200224M15Vpbr_1.csv",
              "200224M16Vpbr_1.csv","200224M17Vpbr_1.csv","200224M21Vpbr_1.csv","200224M22Vpbr_1.csv","200224M23Vpbr_1.csv",
              "200224M24Vpbr_1.csv","200224M25Vpbr_1.csv","200224M26Vpbr_1.csv","200224M31Vpbr_1.csv","200224M32Vpbr_1.csv",
              "200224M33Vpbr_1.csv","200224M34Vpbr_1.csv","200224M36Vpbr_1.csv"]
MxFilesB05 = ["200708M11Vpbr_1.csv","200708M13Vpbr_1.csv","200708M14Vpbr_1.csv","200708M18Vpbr_1.csv","200708M12Vpbr_1.csv",
              "200708M15Vpbr_1.csv","200708M16Vpbr_1.csv","200708M21Vpbr_1.csv","200708M23Vpbr_1.csv","200708M24Vpbr_1.csv",
              "200708M28Vpbr_1.csv","200708M22Vpbr_1.csv","200708M25Vpbr_1.csv","200708M31Vpbr_1.csv","200708M33Vpbr_1.csv",
              "200708M37Vpbr_1.csv","200708M36Vpbr_1.csv"]
MxFilesB100 = ["200605M11Vpbr_1.csv","200605M13Vpbr_1.csv","200605M14Vpbr_1.csv","200605M17Vpbr_1.csv","200605M18Vpbr_1.csv"]
MX100Sim = ["200812M11Vpbr_1.csv","200812M12Vpbr_1.csv","200812M13Vpbr_1.csv","200812M14Vpbr_1.csv",
            "200812M15Vpbr_1.csv","200812M16Vpbr_1.csv","200812M17Vpbr_1.csv","200812M18Vpbr_1.csv"]
MX100mCBP = ["200812M31Vpbr_1.csv","200812M33Vpbr_1.csv","200812M34Vpbr_1.csv","200812M38Vpbr_1.csv","200812M37Vpbr_1.csv"]

MxFiles = MxFilesB00 + MxFilesB00_2  + MxFilesB20 + MxFilesB100 + MxFilesB10 + MxFilesB05 + ["200823M36Vpbr_1.csv"]
MxCols = ["black"]*len(MxFilesB00)+["grey"]*len(MxFilesB00_2)+["green"]*len(MxFilesB20)+\
         ["red"]*len(MxFilesB100)+["lightblue"]*len(MxFilesB10)+["brown"]*len(MxFilesB05) + ["blue"] + ["pink"]*8

colsBSBf=["red"]*len(BSBfilesF0)+["tomato"]*len(BSBfilesF30)+["lightcoral"]*len(BSBfilesF50)+["pink"]*len(BSBfilesF100)
filesBSBf= BSBfilesF0 + BSBfilesF30 + BSBfilesF50 + BSBfilesF100 + ["200527M21Vpfr_1.csv"]

colsBSBx=["black"]*len(BSBfilesF0)+["blue"]*len(BSBfilesF30)+["cornflowerblue"]*len(BSBfilesF50)+\
         ["lightskyblue"]*len(BSBfilesF100) + ["brown","green"]*1 + ["orange","purple"]
filesBSBx=BSBfilesF0+BSBfilesF30+BSBfilesF50+BSBfilesF100 + ["200807M11Vpbr_1.csv"]

cols = MxCols
files = MxFiles

#cols=["green"]*7+["black"]*30
#files=["200517M11Vpbr_1.csv","200517M13Vpbr_1.csv","200517M14Vpbr_1.csv","200517M18Vpbr_1.csv","200517M17Vpbr_1.csv",
       #"200517M12Vpbr_1.csv","200517M15Vpbr_1.csv","200517M16Vpbr_1.csv"]

mCBPfiles = mCBPTC50+mCBPTC25+mCBPTC00+mCBPTH25+mCBPTH50
mCBPcols = ["blue"]*len(mCBPTC50)+["deepskyblue"]*len(mCBPTC25)+["grey"]*len(mCBPTC00) \
            +["darkorange"]*len(mCBPTH25)+["red"]*len(mCBPTH50)
cols2=mCBPcols+["black","green","black","red","brown","yellow"]
files2=mCBPfiles+["200114M16Vpbr_1.csv"]

cols3 = mCBPcolsA + ["green"]*len(mx10) + ["black"]
files3 = mCBPfilesA + mx10 + ["200114M27Vpbr_1.csv"]

OLEDTools.multipleQuenchPlot("V",files,cols,"V")
#OLEDTools.quenchAnalyzePL(files[0],2)`
