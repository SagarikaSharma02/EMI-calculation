#!/usr/bin/env python
# coding: utf-8

# # The os module in Python provides many functions for interacting with the OS and the filesystem. Let's import it and try out some examples.¶

# In[1]:


import os
os.getcwd() #cwd stands for current working directory


# # To get the list of files in a directory, use os.listdir. You pass an absolute or relative path of a directory as the argument to the function.

# In[2]:


help(os.listdir)


# In[3]:


os.listdir('.')


# In[8]:


os.makedirs('./data',exist_ok = True)


# # A new directory can be created using os.makedirs. Let's create a new directory called data, where we'll later download some files.

# In[10]:


'data' in os.listdir('.')


# In[11]:


os.listdir('./data')


# In[12]:


url1 = 'https://hub.jovian.ml/wp-content/uploads/2020/08/loans1.txt'
url2 = 'https://hub.jovian.ml/wp-content/uploads/2020/08/loans2.txt'
url3 = 'https://hub.jovian.ml/wp-content/uploads/2020/08/loans3.txt'


# In[13]:


import urllib.request


# In[18]:


urllib.request.urlretrieve(url1,'./data/loans1.txt')
urllib.request.urlretrieve(url2,'./data/loans2.txt')
urllib.request.urlretrieve(url3,'./data/loans3.txt')


# # Reading from a file

# In[22]:


file1 = open('./data/loans1.txt',mode = 'r')
file1_contents = file1.read()
print(file1_contents)
file1.close()


# # Closing files automatically using with¶

# In[25]:


with open('./data/loans2.txt') as file2:
    file2_contents = file2.read()
    print(file2_contents)


# To make it easy to automatically close a file once you are done processing it, you can open it using the with statement.

# Reading a file line by line File objects provide a readlines method to read a file line-by-line

# In[28]:


with open('./data/loans3.txt') as file3:
    file3_lines = file3.readlines()

    
file3_lines


# In[32]:


def parse_headers(header_line):
    return header_line.strip().split(',')
headers = parse_headers(file3_lines[0])
print(headers)


# In[34]:


def parse_values(data_line):
    values = []
    for item in data_line.strip().split(','):
        if item == '':
            values.append(0.0)
            
        else:
            values.append(item)
            
    return values 
parse_values(file3_lines[1])


# In[36]:


def create_item_dict(values, headers):
    result = {}
    for value, header in zip(values, headers):
        result[header] = value
    return result
values1 = parse_values(file3_lines[1])
create_item_dict(values1, headers)


# # Project

# In[49]:


def parse_headers(header_line):
    return header_line.strip().split(',')

def parse_values(data_line):
    values = []
    for item in data_line.strip().split(','):
        if item == '':
            values.append(0.0)
        
        else:
            values.append(float(item))
            
    return values  
    
def create_dict_item(values,headers):
    result = {}
    for value,header in zip(values,headers):
        result[header] = value
        
    return result    

def read_csv(path):
    result = []
    with open(path,'r') as f:
        lines = f.readlines()
        headers = parse_headers(lines[0])
        
        for data_line in lines[1:]:
            values = parse_values(data_line)
            item_dict = create_dict_item(values,headers)
            result.append(item_dict)
            
    return result        
        


# In[50]:


import math

def loan_emi(amount,duration,rate,down_payment = 0):
    loan_amount = amount - down_payment
    try:
        emi = loan_amount*rate*((1+rate)**duration) / (((1+rate)**duration)-1)
        
    except ZeroDivisionError:
        emi = loan_amount/duration
        
    emi = math.ceil(emi)
    return emi


# In[51]:


loans2 = read_csv('./data/loans2.txt')
loans2


# In[52]:


loans2


# In[53]:


for loan in loans2:
    loan['emi'] = loan_emi(loan['amount'], 
                           loan['duration'], 
                           loan['rate']/12, # the CSV contains yearly rates
                           loan['down_payment'])


# In[54]:


def compute_emis(loans):
    for loan in loans:
        loan['emi'] = loan_emi(
            loan['amount'], 
            loan['duration'], 
            loan['rate']/12, # the CSV contains yearly rates
            loan['down_payment'])


# In[55]:


loans2 = read_csv('./data/loans2.txt')
compute_emis(loans2)
loans2


# # Writing to a file

# In[56]:


with open('./data/emis2.txt', 'w') as f:
    for loan in loans2:
        f.write('{},{},{},{},{}\n'.format(
            loan['amount'], 
            loan['duration'], 
            loan['rate'], 
            loan['down_payment'], 
            loan['emi']))


# In[58]:


file = open('./data/emis2.txt','r')
print(file.read())


# In[7]:


get_ipython().system('pip install jovian --upgrade --quiet')


# In[8]:


import jovian


# In[9]:


jovian.commit(project='python-emi-data-analysis')

