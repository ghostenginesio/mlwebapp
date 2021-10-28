import streamlit as st
import datetime
import numpy as np

st.date_input('Today date',datetime.datetime.now())

import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import os
from  PIL import Image

#
st.title('Homekonnect')
st.header('Data visualization')

data='DailyAttendanceLogsDetails.csv'
df = pd.read_csv(data)
@st.cache(persist=True)

def show_columns(x):
    return x.columns

df.drop(columns=['Punch Records ', 'Overtime', 'Late Entry', 'Early Leave'])
df.rename(columns = {'Employee Code':'Employee_Code', 'Employee Name':'Employee_Name',
                              ' In Time ':'In_Time','Out Time ':'Out_Time'}, inplace = True)
   
df['new_sta'] = df['Status ']
df['new_sta'] = df['new_sta'].apply(lambda x: 0 if x=='Absent'  else 1)
l = list(df['Employee_Name'].unique())


total_days = []
for i in l:
  tem = df[df['Employee_Name'] == i]
  total_days.append(tem.shape[0])
  tem['presenty'] = tem['new_sta'].sum()
  df = pd.concat([tem, df], axis = 0)
df = df.sort_values('presenty', ascending=False)

def plot():
    plt.figure(figsize = (20,10))


    sns.set(font_scale=10)
    sns.set_theme(style="darkgrid")

    fig, ax = plt.subplots()
    ax = sns.barplot(y='Employee_Name', x= 'presenty', data=df, errwidth = 0.5)

    ax.set_title("Total working days "+str(max(total_days)))
    ax.set_xlabel("Presenty fraction", fontsize = 20)
    ax.set_ylabel("Employee name", fontsize = 20)
    st.pyplot(fig)



df['Date'] = df['Date'].apply(pd.to_datetime)


df['In_Time'] = df['In_Time'].fillna("0:0")
df['Out_Time'] = df['Out_Time'].fillna("0:0")
df['Enter_hour'] = df['In_Time'].apply(lambda x: str(x).split(":")[0])
df['Enter_minute'] = df['In_Time'].apply(lambda x: str(x).split(":")[1])

df['leave_hour'] = df['Out_Time'].apply(lambda x: str(x).split(":")[0])
df['leave_minute'] = df['Out_Time'].apply(lambda x: str(x).split(":")[1])

df['Duration_hour'] = df[' Duration '].apply(lambda x: str(x).split(":")[0])
df['Duration_minute'] = df[' Duration '].apply(lambda x: str(x).split(":")[1])

col = ['Enter_hour', 'Enter_minute', 'leave_hour', 'leave_minute', 'Duration_hour', 'Duration_minute']
for i in col:
    df[i] = df[i].astype(int)

df['entry_time1'] = df['Enter_hour']+round(df['Enter_minute']/100, 3)
df['entry_time2'] = df['Enter_hour']+round(df['Enter_minute']/60, 3)

df['leave_time1'] = df['leave_hour']+round(df['leave_minute']/100, 3)
df['leave_time2'] = df['leave_hour']+round(df['leave_minute']/60, 3)

df['duration_time1'] = df['Duration_hour']+round(df['Duration_minute']/100, 3)
df['duration_time2'] = df['Duration_hour']+round(df['Duration_minute']/60, 3)

def plot1():
    tem = df[df['entry_time1']!=0.0]
    l = list(tem['Employee_Name'].unique())
    ord = []
    enter = []
    early_enter = []
    late_enter = []
    for i in l:
        tem1 = tem[tem['Employee_Name'] == i]
        enter.append(tem1['entry_time1'].mean())
        early_enter.append(tem1['entry_time1'].min())
        late_enter.append(tem1['entry_time1'].max())
        ord.append(i)

    newdf = pd.DataFrame({'order':ord, "Enter":enter})

    newdf = newdf.sort_values('Enter', ascending=False)

    ord = list(newdf['order'])

    plt.figure(figsize = (20,10))
    fig, ax = plt.subplots()


    sns.set(font_scale=10)
    sns.set_theme(style="whitegrid")
    ax = sns.barplot(y='Employee_Name', x= 'entry_time1', data=tem, errwidth = 1.5,order = ord, color = 'blue',
                 capsize=.4,  estimator=np.mean)

    ax.set(xlim=(min(early_enter)-0.5, max(late_enter)+0.5))

    ax.set_xlabel("Coming time", fontsize = 20)
    ax.set_ylabel("Employee name", fontsize = 20)
    plt.title('Entry Time of the Employers in office')
    plt.axvspan(min(early_enter)-0.5, 9.30, color='green', alpha=0.3, label = 'early in office')

    plt.axvspan(9.30, max(late_enter)+0.5, color='red', alpha=0.3, label = 'late in office')

    plt.legend()
    plt.show()
    st.pyplot(fig)

def plot3():
    import seaborn as sns
    import matplotlib.pyplot as plt

    plt.figure(figsize = (20,10))

    tem = df[df['duration_time2']!=0.0]
    l = list(tem['Employee_Name'].unique())
    ord = []
    working = []

    for i in l:
        tem1 = tem[tem['Employee_Name'] == i]
        working.append(tem1['duration_time2'].sum())
        ord.append(i)

    newdf = pd.DataFrame({'order':ord, "working_time":working})

    newdf = newdf.sort_values('working_time')

    ord = list(newdf['order'])


    fig, ax = plt.subplots()
    sns.set(font_scale=10)
    sns.set_theme(style="darkgrid")


    #ax = sns.barplot(y='Employee Name', x= 'duration_time1', data=df, errwidth = 2, 
    #                 capsize=.2, palette="Blues_d", color="salmon", estimator=np.sum)


    ax = sns.barplot(y='Employee_Name', x= 'duration_time1', data=df, errwidth = 2, order = ord, 
                    capsize=.2, estimator=np.sum)
    ax.set_xlabel("working time", fontsize = 20)
    ax.set_ylabel("Employee name", fontsize = 20)
    st.pyplot(fig)

def plot4(i):
    col = list(df['Employee_Name'].unique())
# Creating dataset
    
    
    fig, ax = plt.subplots()
    office_enter = 9.30
    office_leaving = 19.00
    tem = df[df['Employee_Name']==i]
    days = tem.shape[0]
    present = tem['new_sta'].sum()
    working_hour = tem['duration_time2'].sum()
    late_comming = tem[tem['entry_time1']>office_enter].shape[0]
    eaarly_leaving = tem[tem['leave_time1']<office_leaving].shape[0]


    fig = plt.figure(figsize =( 15, 10))
    plt.subplot(2,2,1)
    days_Lable = ['present', 'Absent']
    day_data = [present, days-present]
    plt.pie(day_data, labels = days_Lable, autopct='%1.0f%%')
    plt.title('Attendence for : '+i)

    plt.subplot(2,2,2)
    days_Lable = ['completed work hours', 'could not complete']
    day_data = [working_hour, ((office_leaving-office_enter)*days) - working_hour ]
    plt.pie(day_data, labels = days_Lable, autopct='%1.0f%%')
    plt.title('completed work hours in given period for : '+i)

    plt.subplot(2,2,3)
    days_Lable = ['could come time', 'come not come on time']
    day_data = [days - late_comming,  late_comming]
    plt.pie(day_data, labels = days_Lable, autopct='%1.0f%%')
    plt.title('Comming time in office for : '+i)



    plt.subplot(2,2,4)
    days_Lable = ['leave after time', 'leave before the time']
    day_data = [days - eaarly_leaving,  eaarly_leaving]
    plt.pie(day_data, labels = days_Lable, autopct='%1.0f%%')
    plt.title('leaving time from office for : '+i)
                    
    st.pyplot(fig)







    
def main():
    

    if st.checkbox('Preview Dataset'):
        if data is not None:
            if st.checkbox('Head'):
                st.dataframe(df.head())
            if st.checkbox('Tail'):
                st.dataframe(df.tail())
            if st.checkbox('Full Dataset'):
                st.dataframe(df)
    
            
    
    if st.checkbox("Total working days of Empployees"):
        st.write(plot())
    if st.checkbox("Entering time of Employees in Office"):
        st.write(plot1())
    if st.checkbox("Leaving time of Employees in Office"):
        st.write(plot3())
    if st.checkbox("Stats regard to Employee Work in Office"):
        col = list(df['Employee_Name'].unique())
        person= st.selectbox('sel',col)
        st.write(plot4(person))
        
        
    
    
       
        
        

if __name__ == '__main__':
	
	main()

        
        
        


        
