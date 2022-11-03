#!/usr/bin/env python
# coding: utf-8

# In[67]:


import pandas as pd
import numpy as np
import pandas as pd
from datetime import datetime
from operator import itemgetter, attrgetter

from datetime import datetime
df = pd.read_excel (r'C:\Users\MParhizkar\OneDrive - Triodos Bank NV\Documents\Myfiles\Documents\Challenge\hiring challenge - fabricated people_data.xlsx')
df. columns = df. columns. str. replace(' ','_')
result=df.head(10)
print(result)


# In[74]:


# none find_missing=pd.isnull(df["Birthdate"]) 
find_missing=pd.isnull(df["Termdate"]) 
df[find_missing]


# In[78]:


#df1: active but termdate < today
df1=df[(df.Employement_Status=='Active')] 
df1=df1[(df1.Termdate < datetime.now())] 

# count: 195 
df1.head()


# In[79]:


#df2: wrong hire_date

today = datetime.today()
df2=df
df2['age'] = df2['Birthdate'].apply(
               lambda x: today.year - x.year - 
               ((today.month, today.day) < (x.month, x.day)) 
               )
df2['Years worked'] = df2['Hire_Date'].apply(
               lambda x: today.year - x.year - 
              ((today.month, today.day) < (x.month, x.day)) 
            )
df2['age_hired']=df2['age'] - df2['Years worked']

df2=df2.sort_values(by=['age_hired'])

df2=df2[(df2.age_hired < 18)] 
# 5672 df2=df2.count()

df2.head()


# In[ ]:




