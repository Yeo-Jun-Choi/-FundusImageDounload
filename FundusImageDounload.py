#!/usr/bin/env python
# coding: utf-8

# # Retinal Fundus Image
# - 총 5개의 Data Set (4.67G)
# - 파이썬 파일과 동일한 폴더에 다운로드 및 정리
#   - 데이터 폴더 : 'Train'
#   - 데이터 관련 CSV파일 : 'Train/Train.tsv'
#   - 분류 결과 설명 파일 : 'Train/Traininfo.html'
# - 데이터 이미지 확장자는 jpg, bmp

import http
import zipfile
import urllib.request
import subprocess as sp
import os
from urllib.error import URLError, HTTPError
import pandas as pd
import glob
import shutil
import csv
import sys
from PIL import Image

# 데이터셋 출처&다운로드 링크
arg = open('UrlList.csv', 'w', encoding='utf=8', newline="")
wr = csv.writer(arg)
wr.writerow(['STARE', 'http://cecas.clemson.edu/~ahoover/stare/images/all-images.zip', 'STARE_Project.zip'])
wr.writerow(['STARE', "http://cecas.clemson.edu/~ahoover/stare/diagnoses/all-mg-codes.txt", 'STARE/info.txt'])
wr.writerow(['STARE', "http://cecas.clemson.edu/~ahoover/stare/diagnoses/diagnoses.html", 'STARE/diagnoses.html'])
wr.writerow(['csfau', 'https://www5.cs.fau.de/fileadmin/research/datasets/fundus-images/all.zip', 'csfau.zip'])
wr.writerow(['csfau', "https://www5.cs.fau.de/fileadmin/research/datasets/fundus-images/allQuality.zip",
            'csfau/test.zip'])
wr.writerow(['Yiweichen04', 'https://github.com/yiweichen04/retina_dataset/archive/master.zip', 'yiweichen04.zip'])
wr.writerow(['ACRIMA', 'https://ndownloader.figshare.com/files/14137700', 'ACRIMA.zip'])
wr.writerow(['Messidor-2', "https://www.ceos-systems.com/file-sharing/IMAGES.zip.001", 'Messidor-2.zip.001'])
wr.writerow(['Messidor-2', 'https://codeload.github.com/Yeo-Jun-Choi/download/zip/main', 'Messidor-2/messidor_data.zip'])
arg.close()

# sys.argv로 추가적인 데이터 셋 받을 때 처리 정의
while (True):
    if (len(sys.argv)==4):
        l = open('UrlList.csv', 'a', newline="",encoding='utf-8')
        l.write(sys.argv[1], sys.argv[2], sys.argv[3])
        l.close()
        break
    elif(len(sys.argv)>4):
        print("다운로드 URL 입력 오류입니다. 양식 (python 'Fundus.py' '데이터명' 'URL' '(필요시)다운로드 파일명')을 지켜주세요.")
    elif(len(sys.argv)==3):
        l = open('UrlList.csv', 'a', newline="", encoding='utf-8')
        sys.argv[3] = sys.argv[2].split('/')[-1]
        l.write(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        break

# 데이터 개수 세기 위한 변수
k = 1

# 폴더 생성 함수
def direct(path):
    try:
        os.makedirs(os.path.join("Train/{}").format(path))
    except FileExistsError:
        pass

# ## Dataset 처리 관련 변수 정의

recode = {
    "Normal": 0,
    "diabetic_retinopathy": 1,
    "glaucomatous": 2,
    "cataract": 3,
    "retina_disease": 4,
    "Hollenhorst_Emboli": 5,
    "Branch_Retinal_Artery_Occlusion": 6,
    "Cilio-Retinal_Artery_Occlusion": 7,
    "Branch_Retinal_Vein_Occlusion": 8,
    "Central_Retinal_Vein_Occlusion": 9,
    "Hemi-Central_Retinal_Vein_Occlusion": 10,
    "Background_Diabetic_Retinopathy": 11,
    "Proliferative_Diabetic_Retinopathy": 12,
    "Arteriosclerotic_Retinopathy": 13,
    "Hyperensive_Retinopathy": 14,
    "Coats": 15,
    "Macroaneurism": 16,
    "Choroidal_Neovascularization": 17,
    "Diabetic_Macular_Edema": 18
}

# Dataset 처리 관련 폴더 생성
def makeInfoHtml():
    df = pd.read_csv('Train/Train.tsv', sep='\t')
    df = pd.DataFrame(df['Background_Diabetic_Retinopathy'].value_counts())
    df_sum = df['Background_Diabetic_Retinopathy'].sum()
    html = df.to_html(justify='center')
    html = '<h1></h1>\n<h1>Dataset 분류 결과(개수)</h1>' + html
    html = html.replace('</tbody>',
                        '<tr>\n<th>The number of data</th>\n<td>{}</td>\n</tr>\n</tbody>'.format(df_sum))

    recode_dic = pd.DataFrame(recode, index=[0])
    df1 = recode_dic.transpose()
    df1 = df1.to_html(justify='center')
    df1
    df1 = '<h1>Dataset 분류 병명</h1>\n' + df1
    df1 = df1.replace("<th>0</th>", "<th>Disease Number</th>")

    with open('Train/Traininfo.html', 'w', newline="") as Traininfo:
        Traininfo.write(df1)
        Traininfo.write(html)
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

# 전체 데이터셋 설명 tsv파일 생성

writedata = open('Train/Train.tsv', 'w', newline="")
fieldnames = ['Filename', 'number', 'desease']
wrt = csv.writer(writedata, fieldnames, delimiter="\t")


# 데이터셋 객체 정의
class data_download:
    def __init__(self, name, http, saving_name):
        self.name = name
        self.http = http
        self.saving_name = saving_name

    # 데이터 폴더 내 모든 폴더 위치 리턴
    def findDataForder(self, forderList):
        resultForder = forderList
        for forder in forderList:
            new_forderlist = list(filter(os.path.isdir, glob.glob(forder+"\*")))
            if new_forderlist:
                resultForder += self.findDataForder(new_forderlist)
        return resultForder

    # 데이터 폴더 내 모든 이미지파일 위치 리턴
    def findAllImage(self, path):
        mainpath = path+'\*'
        allFile = glob.glob(mainpath)
        allForderList = list(filter(os.path.isdir, allFile))
        filelist = []
        if not allForderList:
            filelist = allFile
        else:
            allForderList = [path]+self.findDataForder(allForderList)
            for forder in allForderList:
                filelist += [file for file in list(filter(os.path.isfile, glob.glob(forder))) if
                         file.endswith(".JPG") or file.endswith(".BMP") or file.endswith("jpg") or file.endswith("bmp")]
        return filelist

    # 데이터를 'Train'폴더에 통합. (overlap : 중복 허용 || data : data설명 csv, tsv, txt파일)
    def dividedata(self, filelist, overlap=False, data=None):
        global k
        num = 0
        num1 = 0
        for i in filelist:
            print("실행")
            x = i.split("\\")
            j = x[-1]

            if (overlap and isinstance(data, pd.core.frame.DataFrame)):
                ## dataFrame type
                if (num1 == 0):
                    for i in data.columns:
                        if ('gradable' in i):
                            print("11212실행")
                            grad = data.columns[num1]
                            num1 += 1
                        elif ('dr_grade' in i):
                            dr = data.columns[num1]
                            num1 += 1
                        elif ('dme' in i):
                            dme = data.columns[num1]
                            num1 += 1
                        else:
                            id = data.columns[num1]
                            num1 += 1

                if (data[id][num] == j):
                    if (data[grad][num] == 0.0):
                        num += 1
                        continue
                    if (data[dr][num] != 0):
                        self.copydata(i, j, "Train/diabetic_retinopathy", recode)
                    else:
                        self.copydata(i, j, "Train/Normal", recode)
                    if (data[dme][num] == 1):
                        k -= 1
                        self.copydata(i, j, "Train/Diabetic_Macular_Edema", recode)
                num += 1
            elif (overlap and isinstance(data, list)):
                while ((data[num][0] + 'bmp') or (data[num][0]+'jpg') != j):
                    num += 1
                    if (len(data) == num):
                        break
                if ((data[num][0] + 'bmp') or (data[num][0] +'jpg') == j):
                    if ('0' in data[num][1]):
                        self.copydata(i, j, "Train/Normal", recode)
                    if ('1' in data[num][1]):
                        self.copydata(i, j, 'Train/Hollenhost_Emboli', recode)
                    if ('2' in data[num][1]):
                        self.copydata(i, j, 'Train/Branch_Retinal_Artery_Occlusion', recode)
                    if ('3' in data[num][1]):
                        self.copydata(i, j, 'Train/Cilio-Retinal_Artery_Occlusion', recode)
                    if ('4' in data[num][1]):
                        self.copydata(i, j, 'Train/Branch_Retinal_Vein_Occlusion', recode)
                    if ('5' in data[num][1]):
                        self.copydata(i, j, 'Train/Central_Retinal_Vein_Occlusion', recode)
                    if ('6' in data[num][1]):
                        self.copydata(i, j, 'Train/Hemi-Central_Retinal_Vein_Occlusion', recode)
                    if ('7' in data[num][1]):
                        self.copydata(i, j, 'Train/Background_Diabetic_Retinopathy', recode)
                    if ('8' in data[num][1]):
                        self.copydata(i, j, 'Train/Proliferative_Diabetic_Retinopathy', recode)
                    if ('9' in data[num][1]):
                        self.copydata(i, j, 'Train/Arteriosclerotic_Retinopathy', recode)
                    if ('10' in data[num][1]):
                        self.copydata(i, j, 'Train/Hyperensive_Retinopathy', recode)
                    if ('11' in data[num][1]):
                        self.copydata(i, j, 'Train/Coats', recode)
                    if ('12' in data[num][1]):
                        self.copydata(i, j, 'Train/Macroaneurism', recode)
                    if ('13' in data[num][1]):
                        self.copydata(i, j, 'Train/Choroidal_Neovascularization', recode)
                num += 1

            else:
                if ("_dr" or "_dr_" in i):
                    self.copydata(i, j, "Train/diabetic_retinopathy", recode)
                elif ("_g" or "_g_" or "glaucoma" in i):
                    self.copydata(i, j, "Train/glaucomatous", recode)
                elif ("_c" or "_c_" or "cataract" in i):
                    self.copydata(i, j, "Train/cataract", recode)
                elif ("retina_dissease" in i):
                    self.copydata(i, j, "Train/retina_disease", recode)
                elif ("good" in i):
                    self.copydata(i, j, "Train/Normal", recode)
                else:
                    self.copydata(i, j, "Train/Normal", recode)

    # 데이터 관련 정보 전처리. csv, tsv파일이 있으면 infodata=True
    def Comb(self, path, infodata=False):
        filelist = self.findAllImage(path)
        for i in range(len(filelist)):
            oldname = filelist[i]
            if ('ppm' in oldname):
                newname = os.path.splitext(oldname)[0] + '.bmp'
                image = Image.open(oldname)
                image.save(newname, 'BMP')

        global k

        if(infodata):
            dir_name = path
            for n_path, dirs, files in os.walk(dir_name):
                for filename in files:
                    if 'csv' in filename:
                        data = pd.read_csv(n_path+'/'+filename)
                        break
                    elif 'tsv' in filename:
                        data = pd.read_csv(n_path+'/'+filename, sep='\t')
                        break
                    elif 'txt' in filename:
                        new_filelist = []
                        file = open((n_path+'/'+filename))
                        line = file.readline()
                        while line:
                            new_filelist.append(line)
                            line = file.readline()
                        file.close()
                        for i in range(len(new_filelist)):
                            try:
                                new_filelist[i] = new_filelist[i].split('\t')
                                new_filelist[i][1] = new_filelist[i][1].split(' ')
                            except:
                                try:
                                    new_filelist[i] = new_filelist[i].split(',')
                                    new_filelist[i][1] = new_filelist[i][1].split(' ')
                                except:
                                    break
                        data = new_filelist
            try:
                self.dividedata(filelist, overlap=True, data=data)
            except:
                pass

        else:
            try:
                self.dividedata(filelist)
            except:
                pass

    # 데이터 다운로드
    def downloadUrl(self, http, saving_name):
        try:
            if not os.path.isfile(saving_name):
                urllib.request.urlretrieve(http, saving_name)
                filenameList = http.split('.')
                checkdivide = filenameList[-1]
                if (str(type(int(checkdivide))) == "<class 'int'>"):
                    newSaving_name = saving_name.split('.')
                    checkdivide = int(checkdivide) + 1
                    filenameList[-1] = filenameList[-1][:-1] + str(checkdivide)
                    newSaving_name[-1] = newSaving_name[-1][:-1] + str(checkdivide)
                    self.downloadUrl('.'.join(filenameList), '.'.join(newSaving_name))
        except ValueError:
            pass
        except HTTPError:
            pass

    # 데이터 압축해제. 분할압축일시 divide = True
    def openzip(self, filename, fordername, divide=False):
        name = filename.split('.')
        if divide:
            print("분할압축풀기 시작")
            num = name[-1]
            num1 = int(num)
            fullname = filename
            while True:
                num1 += 1
                num = num[:len(num) - 1] + str(num1)
                name[-1] = num
                if os.path.isfile('.'.join(name)):
                    fullname += "+{}".format('.'.join(name))
                else:
                    name = '.'.join(name[:-1])
                    break
            sp.call("copy /b {0} {1}".format(fullname, name), shell=True)
            files = zipfile.ZipFile(name)
        else:
            try:
                files = zipfile.ZipFile(filename)
            except FileNotFoundError:
                print(filename + "\n올바르지 않는 경로입니다..")
                return
            except zipfile.BadZipFile:
                return
        try:
            files.extractall(fordername)
            files.close()
        except UnboundLocalError:
            pass

    # 파일 이름 변경 (대상 파일, 경로, 바꿀 파일 명, 데이터 번호(k))
    def changeName(self, filename, path, cName, datanum):
        os.rename(path + '/' + filename, path + '/' + str(cName) + str(datanum) + '.jpg')

    # 데이터 복사(파일명+경로, 파일명, 복사할 경로, 복사 할 위치값 dic)
    def copydata(self, file, data, path, recode):
        global k
        disease = path.split('/')[-1]
        shutil.copy2(file, path)
        self.changeName(data, path, 'data', k)
        wrt.writerow(['data{}'.format(k), recode[disease], disease])
        k += 1

    # 데이터 다운로드 & 압축해제 기능 통합
    def downloadDataset(self):
        # 다운로드
        self.downloadUrl(self.http, self.saving_name)

        # 압축 해제(분할 압축 or 일반 압축)
        try:
            a = int(self.saving_name.split('.')[-1])
            self.openzip(self.saving_name, self.name, divide=True)
        except ValueError:
            self.openzip(self.saving_name, self.name)
        except:
            pass

    # 데이터 전처리 기능 통합
    def preAnalysis(self, obj, num):
        # l = open('UrlList.csv', 'r', encoding='utf=8',newline="")
        # rdr = csv.reader(l)
        # obj = []
        # for line in rdr:
        #     a = data_download(line[0], line[1], line[2])
        #     obj.append([a, line[0]])
        # l.close()
        try:
            if (obj[num + 1][1] == obj[num][1]):
                obj[num][0].Comb(obj[num][0].name, infodata=True)
            else:
                obj[num][0].Comb(obj[num][0].name)
        except:
            pass

    #데이터 설명 파일(HTML) 생성


def main():
    f = open('UrlList.csv', 'r', encoding='utf-8',newline="")
    rdr = csv.reader(f)
    obj = []
    for line in rdr:
        data = data_download(line[0],line[1],line[2])
        obj.append([data,line[0]])
        #data.downloadDataset()
    f.close()
    num = 0
    for ob in obj:
        ob[0].preAnalysis(obj,num)
        num+=1
    makeInfoHtml()
    writedata.close()

main()