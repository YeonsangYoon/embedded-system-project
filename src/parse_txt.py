#!/usr/bin/env python
# coding: utf-8

# In[53]:


def parse_result(file_name, threshold):
    f = open(file_name)
    lines = f.readlines()
    lines = lines[1:]
    can = []
    pet = []
    for i in range(len(lines)):
        lines[i] = lines[i].replace(":", "")
        lines[i] = lines[i].replace("%\n", "")
        each = lines[i].split()
        if(each[0] == 'pet'):
            pet.append(int(each[1]))
        else:
            can.append(int(each[1]))
    can_possibility = sum(pet)/len(pet)
    pet_possibility = sum(pet)/len(pet)
    if (max(can_possibility, pet_possibility) < threshold):
        return 0, 0
    elif(can_possibility>pet_possibility):
        return 1, pet_possibility
    else:
        return 2, can_possibility


# In[56]:


petOrCan, possibility = parse_result('D:\workspace_py\darknet_parse\parse_1.txt', 50)
print("this is %d with possibility of %.1f percent " %(petOrCan, possibility))

