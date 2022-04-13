import pandas as pd 
import re

df=pd.read_csv("../TCPD-CMID_1962_2022.csv") 
mdf=pd.read_csv("../../tcpd-data/AE/Analysis_Data/Consolidated_AE_mastersheet_socio.csv",low_memory=False)

def rep(text):
	text=re.sub(" ","_",text)
	text=re.sub("and","&",text)
	return text

#df["State_Name"]=df["state"].apply(rep)

mdf["pid_IED"]=mdf["pid"]
mdf["No_Terms_as_MLA"]=mdf["No_Terms"]
mdf["Education"]=mdf["MyNeta_education"]

df=df[["State_Name","Assembly_No","Sequence_No","pid_CM","No_Terms_as_CM","Name","Start_Date","End_Date","Days_in_Office","Appointment_Delay","Administrative_Rule","MLC","Caretaker_CM","Constituency_No","Poll_No","Position"]]
mdf=mdf[["State_Name","Assembly_No","Constituency_No","Poll_No","Position","Constituency_Name","pid_IED","Party","No_Terms_as_MLA","Turncoat","Incumbent","Recontest","TCPD_Prof_Main","Education"]]

df2=df.merge(mdf, on=["State_Name","Assembly_No","Constituency_No","Poll_No","Position"], how="left")

df2.to_csv("../TCPD-CMID_1962_2022.csv",index=False)