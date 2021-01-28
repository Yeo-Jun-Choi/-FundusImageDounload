# -FundusImageDownload

There are 5 datasets
 - STARE dataset : http://cecas.clemson.edu/
 - yiweichen04's dataset : https://github.com/yiweichen04/retina_dataset
 - csfau dataset : https://www5.cs.fau.de/
 - ACRIMA dataset : https://ndownloader.figshare.com/-
 - Messider-2 dataset : https://www.ceos-systems.com/

If you run this code, Your computer takes them and classify each disease name.
 - Data forder = 'Train'
 - CSV of data = 'Train/Train.csv'
 - Explaining of data = 'Train/Traininfo.html'
 - File extension = .jpg or .bmp


All of them is 4.85G. so your hard disk must have about 10G free space.

If you have additional dataset, you can add it when you run this.

 Ex) python FundusImageDownload.py 'Dataname', 'https:', 'savingName.zip'
or Revise 'UrlList.csv'
(when you run this code, the csv file is formed)

If your additional dataset has csv, tsv or txt, You also have to add it.

Thanks.
