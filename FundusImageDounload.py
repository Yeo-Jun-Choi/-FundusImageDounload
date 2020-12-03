#!/usr/bin/env python
# coding: utf-8

# # Retinal Fundus Image
# - 총 5개의 Data Set (4.67G)
# - 파이썬 파일과 동일한 폴더에 다운로드 및 정리
#   - 데이터 폴더 : 'Train'
#   - 데이터 관련 CSV파일 : 'Train/Train.tsv'
#   - 분류 결과 설명 파일 : 'Train/Traininfo.html'
# - 데이터 이미지 확장자는 jpg, bmp

# In[1]:


import zipfile
import urllib.request
import subprocess as sp
import os
from urllib.error import URLError, HTTPError
from PIL import Image
import pandas as pd
import numpy as np
import glob
import shutil
import csv
k = 1


# ## 데이터 다운로드 함수

# In[83]:


def dounloadUrl(http, saving_name):
    try:
        urllib.request.urlretrieve(http,saving_name)
    except HTTPError:
        print(http+"\n위 사이트에 문제가 생겨 파일을 찾을 수 없습니다.")
        pass


# ## 압축파일 해제 함수(분할압축파일은 divide = True로 변경)

# In[34]:


def openzip(filename, fordername, divide=False):
    if divide:
        name = filename.split('.')
        num = name[-1]
        num1 = int(num)
        fullname = filename
        while True :
            num1 += 1 
            num = num[:len(num)-1]+str(num1)
            name[-1] = num
            if os.path.isfile('.'.join(name)):
                fullname+="+{}".format('.'.join(name))
            else:
                break
        name = name[0]+'.zip'
        sp.call("copy /b {0} {1}".format(fullname,name), shell=True)
        files = zipfile.ZipFile(name)
    else:
        try:
            files = zipfile.ZipFile(filename)
        except FileNotFoundError:
            print(filename+"\n올바르지 않는 경로입니다..")
            pass
        except zipfile.BadZipFile:
            print("올바르지 않는 압축 파일입니다.")
            pass
    files.extractall(fordername)
    files.close()


# ## Train 폴더 내 새로운 폴더 생성 함수

# In[85]:


def direct(path):
    try:
        os.makedirs(os.path.join("Train/{}").format(path))
    except FileExistsError:
        pass


# ## 파일 이름 바꾸는 함수

# In[86]:


def changeName(filename, path, cName, datanum):
    os.rename(path+'/'+filename, path+'/'+str(cName)+str(datanum)+'.jpg')


# ## 특정 위치로 파일 복사

# In[87]:


def copydata(file, data, path, recode):
    global k
    disease = path.split('/')[-1]
    shutil.copy2(file, path)
    changeName(data, path, 'data', k)
    wr.writerow(['data{}'.format(k),recode[disease],disease])
    k+=1


# ## csfau Dataset 처리

# In[88]:


def csfau_comb(path):
    cs_files = list(filter(os.path.isfile,glob.glob(path)))
    for i in cs_files:
        x = i.split('\\')
        j = x[-1]
        if("_dr" in i):
            copydata(i, j, dr, recode)
        elif("_g" in i):
            copydata(i, j, g, recode)
        else:
            copydata(i, j, n, recode)

def csfau_t_comb(path):
    cs_test = list(filter(os.path.isfile, glob.glob(path)))
    for i in cs_test:
        x = i.split('\\')
        j = x[-1]
        if("good"in i):
            copydata(i, j, n, recode)


# ## ACRIMA Dataset 처리

# In[89]:


def db_comb(path):
    db_files = list(filter(os.path.isfile,glob.glob(path)))
    for i in db_files:
        x = i.split('\\')
        j = x[-1]
        if("_g_" in j):
            copydata(i, j, g, recode)
        else:
            copydata(i, j, n, recode)


# ## yiweichen04 Dataset 처리

# In[90]:


def Yi_comb(path):
    Yi_files = list(filter(os.path.isfile,glob.glob(path)))
    if('1_normal' in path):
        for i in Yi_files:
            x = i.split('\\')
            j = x[-1]
            copydata(i, j, n, recode)
            
    elif('2_cataract' in path):
        for i in Yi_files:
            x = i.split("\\")
            j = x[-1]
            copydata(i, j, c, recode)
            
    elif('2_glaucoma' in path):
        for i in Yi_files:
            x = i.split("\\")
            j = x[-1]
            copydata(i, j, g, recode)
            
    elif('3_retina_disease' in path):
        for i in Yi_files:
            x = i.split("\\")
            j = x[-1]
            copydata(i, j, r, recode)


# ## STARE_save Dataset 처리

# In[91]:


def STARE_save(data, cName, recode):
    global k
    data.save("Train/{0}/data{1}.bmp".format(cName,k))
    wr.writerow(['data{}'.format(k), recode[cName], cName])
    k+=1


# In[92]:


def STARE_combi(path):
    STARE_im = list(filter(os.path.isfile,glob.glob(path)))
    filelist = []
    file = open("STARE/info.txt")
    m = file.readline()
    while m:
        filelist.append(m)
        m = file.readline()
    for i in range(len(filelist)):
        filelist[i] = filelist[i].split('\t')
    for i in range(len(filelist)):
        filelist[i][1] = filelist[i][1].split(" ")
    file.close()
    
    
    num = 0
    for i in STARE_im:
        x = i.split("\\")
        j = x[-1]
    
        if not ('ppm' in i):
            continue
    
        while((filelist[num][0]+".ppm") != j):
            num+=1
            if(len(filelist)==num):
                break
        im = Image.open(i)
        
        if((filelist[num][0]+".ppm") == j):
            if('0' in filelist[num][1]):
                STARE_save(im, 'Normal',recode)
            if('1' in filelist[num][1]):
                STARE_save(im, 'Hollenhorst_Emboli',recode)
            if('2' in filelist[num][1]):
                STARE_save(im, 'Branch_Retinal_Artery_Occlusion',recode)
            if('3' in filelist[num][1]):
                STARE_save(im, 'Cilio-Retinal_Artery_Occlusion',recode) 
            if('4' in filelist[num][1]):
                STARE_save(im, 'Branch_Retinal_Vein_Occlusion',recode)
            if('5' in filelist[num][1]):
                STARE_save(im, 'Central_Retinal_Vein_Occlusion',recode)
            if('6' in filelist[num][1]):
                STARE_save(im, 'Hemi-Central_Retinal_Vein_Occlusion',recode)
            if('7' in filelist[num][1]):
                STARE_save(im, 'Background_Diabetic_Retinopathy',recode)
            if('8' in filelist[num][1]):
                STARE_save(im, 'Proliferative_Diabetic_Retinopathy',recode)
            if('9' in filelist[num][1]):
                STARE_save(im, 'Arteriosclerotic_Retinopathy',recode)
            if('10' in filelist[num][1]):
                STARE_save(im, 'Hyperensive_Retinopathy',recode)
            if('11' in filelist[num][1]):
                STARE_save(im, 'Coats',recode)
            if('12' in filelist[num][1]):
                STARE_save(im, 'Macroaneurism',recode)
            if('13' in filelist[num][1]):
                STARE_save(im, 'Choroidal_Neovascularization',recode)
        num+=1
        im.close()


# ## Messidor-2 Dataset 처리

# In[93]:


def messi_combi(path):
    global k
    data = pd.read_csv("Messidor-2/dounload-main/messidor_data.csv")

    Messidor = list(filter(os.path.isfile,glob.glob(path)))
    num = 0

    for i in Messidor:
        x = i.split('\\')
        j = x[-1]
        if(data["image_id"][num] == j):
            if(data["adjudicated_gradable"][num]==0.0):
                num+=1
                continue
            
            if(data["adjudicated_dr_grade"][num]!=0):
                copydata(i, j, dr, recode)
            else:
                copydata(i, j, n, recode)
            if(data["adjudicated_dme"][num]==1):
                k-=1
                copydata(i, j, dme, recode)
        num+=1


# ## Dataset 처리 관련 변수 정의

# In[151]:


recode = {
    "Normal" : 0,
    "diabetic_retinopathy":1,
    "glaucomatous":2,
    "cataract":3,
    "retina_disease":4,
    "Hollenhorst_Emboli":5,
    "Branch_Retinal_Artery_Occlusion":6,
    "Cilio-Retinal_Artery_Occlusion":7,
    "Branch_Retinal_Vein_Occlusion":8,
    "Central_Retinal_Vein_Occlusion":9,
    "Hemi-Central_Retinal_Vein_Occlusion":10,
    "Background_Diabetic_Retinopathy":11,
    "Proliferative_Diabetic_Retinopathy":12,
    "Arteriosclerotic_Retinopathy":13,
    "Hyperensive_Retinopathy":14,
    "Coats":15,
    "Macroaneurism":16,
    "Choroidal_Neovascularization":17,
    "Diabetic_Macular_Edema" : 18
}


# In[95]:


dr = "Train/diabetic_retinopathy"
g = "Train/glaucomatous"
n = "Train/Normal"
c = "Train/cataract"
r = "Train/retina_disease"
dme = "Train/Diabetic_Macular_Edema"


# ## Dataset 처리 관련 폴더 생성

# In[96]:


try:
    os.makedirs(os.path.join("Train"))
except:
    pass
direct("diabetic_retinopathy")
direct("glaucomatous")
direct("Normal")
direct("cataract")
direct("retina_disease")
direct("Hollenhorst_Emboli")
direct("Branch_Retinal_Artery_Occlusion")
direct("Cilio-Retinal_Artery_Occlusion")
direct("Branch_Retinal_Vein_Occlusion")
direct("Central_Retinal_Vein_Occlusion")
direct("Hemi-Central_Retinal_Vein_Occlusion")
direct("Background_Diabetic_Retinopathy")
direct("Proliferative_Diabetic_Retinopathy")
direct("Arteriosclerotic_Retinopathy")
direct("Hyperensive_Retinopathy")
direct("Coats")
direct("Macroaneurism")
direct("Choroidal_Neovascularization")
direct("Diabetic_Macular_Edema")


# ## 전체 데이터셋 관련 tsv파일

# In[97]:


f = open('Train/Train.tsv','w')
fieldnames = ['Filename', 'number', 'desease']
wr = csv.writer(f, fieldnames, delimiter = "\t")


# ## STARE Dataset dounload & open

# In[98]:


def STARE(http, saving_name, fordername):
    dounloadUrl(http, saving_name)
    openzip(saving_name, fordername)
    dounloadUrl("http://cecas.clemson.edu/~ahoover/stare/diagnoses/all-mg-codes.txt",'STARE/info.txt')
    dounloadUrl("http://cecas.clemson.edu/~ahoover/stare/diagnoses/diagnoses.html",'STARE/diagnoses.html')
    STARE_combi(fordername+'/*')


# ## csfau Dataset dounload & open

# In[99]:


def csfau(http, saving_name, fordername):
    dounloadUrl(http, saving_name)
    openzip(saving_name, fordername)
    dounloadUrl("https://www5.cs.fau.de/fileadmin/research/datasets/fundus-images/allQuality.zip", 'csfau/test.zip')
    openzip('csfau/test.zip','test')
    csfau_comb(fordername+'/image/*')
    csfau_t_comb(fordername+'/test/*')


# ## yiweichen04 Dataset dounload & open

# In[100]:


def yiweichen04(http, saving_name, fordername):
    dounloadUrl(http, saving_name)
    openzip(saving_name, fordername)
    Yi_comb(fordername+'/retina_dataset-master/dataset/1_normal/*')
    Yi_comb(fordername+'/retina_dataset-master/dataset/2_cataract/*')
    Yi_comb(fordername+'/retina_dataset-master/dataset/2_glaucoma/*')
    Yi_comb(fordername+'/retina_dataset-master/dataset/3_retina_disease/*')


# ## ACRIMA Dataset dounload & open

# In[101]:


def ACRIMA(http, saving_name, fordername):
    dounloadUrl(http, saving_name)
    openzip(saving_name, fordername)
    db_comb(fordername+'/Database/Images/*')


# ## Messidor-2 Dataset dounload & open

# In[102]:


def Messidor(http, saving_name, fordername):
    https = http[:len(http)-1]
    savename = saving_name[:len(saving_name)-1]
    
    dounloadUrl(https+'1', savename+'1')
    dounloadUrl(https+'2', savename+'2')
    dounloadUrl(https+'3', savename+'3')
    dounloadUrl(https+'4', savename+'4')
    dounloadUrl('https://codeload.github.com/Yeo-Jun-Choi/dounload/zip/main','Messidor-2/messidor_data.zip')
    openzip(saving_name, fordername, divide=True)
    openzip('Messidor-2/dounload-main.zip','Messidor-2')
    messi_combi(fordername+'/IMAGES/*')


# In[103]:


def main():
    STARE('http://cecas.clemson.edu/~ahoover/stare/images/all-images.zip', 'STARE_Project.zip', 'STARE')
    csfau('https://www5.cs.fau.de/fileadmin/research/datasets/fundus-images/all.zip', 'csfau.zip','csfau')
    yiweichen04('https://github.com/yiweichen04/retina_dataset/archive/master.zip','yiweichen04.zip','Yiweichen04')
    ACRIMA('https://ndownloader.figshare.com/files/14137700','database.zip','database')
    Messidor("https://www.ceos-systems.com/file-sharing/IMAGES.zip.001",'Messidor-2.zip.001','Messidor-2')
    


# In[104]:


#main()
f.close()


# ## Dataset 설명하는 html파일 작성

# In[192]:


df = pd.read_csv('Train/Train.tsv', sep='\t')
df = pd.DataFrame(df['Background_Diabetic_Retinopathy'].value_counts())
df_sum = df['Background_Diabetic_Retinopathy'].sum()
html = df.to_html(justify='center')
html = '<h1></h1>\n<h1>Dataset 분류 결과(개수)</h1>'+html
html = html.replace('</tbody>','<tr>\n<th>The number of data</th>\n<td>{}</td>\n</tr>\n</tbody>'.format(df_sum))


# In[193]:


recode_dic = pd.DataFrame(recode, index=[0])
df1 = recode_dic.transpose()
df1 = df1.to_html(justify = 'center')
df1
df1 = '<h1>Dataset 분류 병명</h1>\n'+df1
df1 = df1.replace("<th>0</th>","<th>Disease Number</th>")


# In[194]:


with open('Train/Traininfo.html', 'w') as Traininfo:
    Traininfo.write(df1)
    Traininfo.write(html)

