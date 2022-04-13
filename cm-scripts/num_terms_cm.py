import re
import pandas as pd
from datetime import datetime

df=pd.read_csv("../TCPD-CMID_1962_2022.csv")

#df=df[df.acting==0]

repeat_o=df['pid_CM'].value_counts().to_dict()
repeat=df['pid_CM'].value_counts().to_dict()

for index, row in df.iterrows():
	pid_CM=row["pid_CM"]
	try:
			if(repeat[pid_CM]>0):
					x=1+repeat_o[pid_CM]-repeat[pid_CM]
					repeat[pid_CM]-=1
					df.loc[index,"No_Terms_as_CM"]=x
	except:
			print("pid_CM")
			print(pid_CM)

def fix_time(text):
	if text!="Current":
		tv=datetime.strptime(text,"%d-%m-%Y")
		fv=datetime.strftime(tv,"%Y-%m-%d")
	else:
		fv="Current"
	return fv

def get_time(text):
	if text=="Current":
		text="2022-04-05"
	try:
		tv=datetime.strptime(text,"%Y-%m-%d")
	except:
		tv=text
	return tv

def clean_days(text):
	text=str(text)
	try:
		t=re.sub(" days 00:00:00"," ",text)
		t=int(t)
	except:
		t="NA"
	return t

df["Start_Date"]=df["Start_Date"].apply(fix_time)
df["End_Date"]=df["End_Date"].apply(fix_time)

df["start"]=df["Start_Date"].apply(get_time)
df["end"]=df["End_Date"].apply(get_time)
df["Days_in_Office"]=df["end"]-df["start"]
df["Days_in_Office"]=df["Days_in_Office"].apply(clean_days)

states=list(set(df["State_Name"].tolist()))

for s in states:
	sdf=df[df.State_Name==s]
	sdf=sdf.reset_index()
	for x in range(1,len(sdf)):
		prev=sdf.iloc[x-1]["end"]
		this=sdf.iloc[x]["start"]
		ind=sdf.iloc[x]["index"]
		df.loc[ind,"Appointment_Delay"]=this-prev

df["Appointment_Delay"]=df["Appointment_Delay"].apply(clean_days)

df=df[["State_Name","Assembly_No","Sequence_No","pid_CM","No_Terms_as_CM","Name","Start_Date","End_Date","Days_in_Office","Appointment_Delay","Administrative_Rule","MLC","Caretaker_CM","Constituency_No","Poll_No","Position","Constituency_Name","pid_IED","Party","No_Terms_as_MLA","Turncoat","Incumbent","Recontest","TCPD_Prof_Main","Education"]]

df.to_csv("../TCPD-CMID_1962_2022.csv",index=False)
