#!/usr/bin/env python
# coding: utf-8

# # EMI Calculation
# 

# # The os module in Python provides many functions for interacting with the OS and the filesystem. Let's import it and try out some examples.

# In[21]:


import os


# In[22]:


os.getcwd() #cwd stands for current working directory


# # To get the list of files in a directory, use os.listdir. You pass an absolute or relative path of a directory as the argument to the function.
# 
# 

# In[23]:


help(os.listdir)


# In[24]:


os.listdir('.')


# In[25]:


os.listdir('/usr/lib')


# # A new directory can be created using os.makedirs. Let's create a new directory called data, where we'll later download some files.

# In[26]:


os.makedirs('./data', exist_ok=True)


# In[27]:


help(exist_ok)


# In[28]:


'data' in os.listdir('.')


# In[29]:


os.listdir('./data')


# In[30]:


url1 = 'https://hub.jovian.ml/wp-content/uploads/2020/08/loans1.txt'
url2 = 'https://hub.jovian.ml/wp-content/uploads/2020/08/loans2.txt'
url3 = 'https://hub.jovian.ml/wp-content/uploads/2020/08/loans3.txt'


# In[31]:


import urllib.request


# In[32]:


urllib.request.urlretrieve(url1, './data/loans1.txt')


# In[33]:


urllib.request.urlretrieve(url2, './data/loans2.txt')


# In[34]:


urllib.request.urlretrieve(url3, './data/loans3.txt')


# # Reading from a file
# To read the contents of a file, we first need to open the file using the built-in open function. The open function returns a file object, provides several methods for interacting with the contents of the file. It also accepts a mode argument

# In[35]:


file1 = open('./data/loans1.txt', mode='r')


# In[36]:


file1_contents = file1.read()


# In[37]:


print(file1_contents)


# In[38]:


file1.close()


# In[39]:


file1.read()


# # Closing files automatically using with
# To make it easy to automatically close a file once you are done processing it, you can open it using the with statement.

# In[40]:


with open('./data/loans2.txt') as file2:
    file2_contents = file2.read()
    print(file2_contents)


# Once the statements within the with block are executed, the .close method on file2 is automatically invoked. Let's verify this by trying to read from the file object again.

# In[41]:


file2.read()


# Reading a file line by line
# File objects provide a readlines method to read a file line-by-line

# In[42]:


with open('./data/loans3.txt') as file3:
    file3_lines = file3.readlines()
    #print(file3_lines)


# In[43]:


file3_lines


# In[44]:


file3_lines[0]


# In[45]:


file3_lines[0].strip()


# In[46]:


print(file2_contents)


# In[47]:


'828400,120,0.11,100000'.split(',')


# In[48]:


loan1 = {
    'amount':828400,
    'duration':120,
    'rate':0.11,
    'down_payment':100000
}


# In[49]:


def parse_headers(header_line):
    return header_line.strip().split(',')


# In[50]:


headers = parse_headers(file3_lines[0])
print(headers)


# In[51]:








def parse_values(data_line):
    values = []
    for item in data_line.strip().split(','):
        values.append(float(item))
    return values


# In[52]:


file3_lines[2]


# In[53]:


parse_values(file3_lines[2])


# In[54]:


def parse_values(data_line):
    values = []
    for item in data_line.strip().split(','):
        if item == '':
            values.append(0.0)
        else:
            values.append(float(item))
    return values


# In[55]:


parse_values(file3_lines[1])


# In[56]:


def create_item_dict(values, headers):
    result = {}
    for value, header in zip(values, headers):
        result[header] = value
    return result


# In[57]:


file3_lines[1]


# In[58]:


values1 = parse_values(file3_lines[1])
create_item_dict(values1, headers)


# In[59]:


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

def create_item_dict(values, headers):
    result = {}
    for value, header in zip(values, headers):
        result[header] = value
    return result

def read_csv(path):
    result = []
    # Open the file in read mode
    with open(path, 'r') as f:
        # Get a list of lines
        lines = f.readlines()
        # Parse the header
        headers = parse_headers(lines[0])
        # Loop over the remaining lines
        for data_line in lines[1:]:
            # Parse the values
            values = parse_values(data_line)
            # Create a dictionary using values & headers
            item_dict = create_item_dict(values, headers)
            # Add the dictionary to the result
            result.append(item_dict)
    return result


# In[60]:


import math

def loan_emi(amount, duration, rate, down_payment=0):
    """Calculates the equal montly installment (EMI) for a loan.
    
    Arguments:
        amount - Total amount to be spent (loan + down payment)
        duration - Duration of the loan (in months)
        rate - Rate of interest (monthly)
        down_payment (optional) - Optional intial payment (deducted from amount)
    """
    loan_amount = amount - down_payment
    try:
        emi = loan_amount * rate * ((1+rate)**duration) / (((1+rate)**duration)-1)
    except ZeroDivisionError:
        emi = loan_amount / duration
    emi = math.ceil(emi)
    return emi


# In[61]:


loans2 = read_csv('./data/loans2.txt')


# In[62]:


loans2


# In[63]:


for loan in loans2:
    loan['emi'] = loan_emi(loan['amount'], 
                           loan['duration'], 
                           loan['rate']/12, # the CSV contains yearly rates
                           loan['down_payment'])


# In[64]:


def compute_emis(loans):
    for loan in loans:
        loan['emi'] = loan_emi(
            loan['amount'], 
            loan['duration'], 
            loan['rate']/12, # the CSV contains yearly rates
            loan['down_payment'])


# In[65]:


loans2 = read_csv('./data/loans2.txt')


# In[66]:


compute_emis(loans2)


# In[67]:


loans2


# In[68]:


with open('./data/emis2.txt', 'w') as f:
    for loan in loans2:
        f.write('{},{},{},{},{}\n'.format(
            loan['amount'], 
            loan['duration'], 
            loan['rate'], 
            loan['down_payment'], 
            loan['emi']))


# In[69]:


os.listdir('data')


# In[70]:


with open('./data/emis2.txt', 'r') as f:
    print(f.read())


# In[71]:


def write_csv(items, path):
    # Open the file in write mode
    with open(path, 'w') as f:
        # Return if there's nothing to write
        if len(items) == 0:
            return
        
        # Write the headers in the first line
        headers = list(items[0].keys())
        f.write(','.join(headers) + '\n')
        
        # Write one item per line
        for item in items:
            values = []
            for header in headers:
                values.append(str(item.get(header, "")))
            f.write(','.join(values) + "\n")


# In[72]:


loans3 = read_csv('./data/loans3.txt')


# In[73]:


compute_emis(loans3)


# In[74]:


write_csv(loans3, './data/emis3.txt')


# In[75]:


with open('./data/emis3.txt', 'r') as f:
    print(f.read())


# In[76]:


for i in range(1,4):
    loans = read_csv('./data/loans{}.txt'.format(i))
    compute_emis(loans)
    write_csv(loans, './data/emis{}.txt'.format(i))


# In[77]:


os.listdir('./data')

