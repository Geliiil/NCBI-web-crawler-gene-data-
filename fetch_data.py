import requests
from xml.etree.ElementTree import fromstring, ElementTree
import os
import time
from tqdm import tqdm
os.chdir("/data") #data folder path
def fetch_data(name,Accessions):
  IDs =[]
  ncbi_url = "https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?"
  #get GI
  for ac in Accessions:
    r = requests.get(f"https://www.ncbi.nlm.nih.gov/nuccore/{ac}?report=gilist&log$=seqview&format=text")
    tree = ElementTree(fromstring(r.text))
    GI = tree.getroot().text.replace("\n","")
    IDs.append(GI)
    time.sleep(1.5)
  print(IDs) 
  #get data
  params ={
    'tool':'portal',
    'save':'file',
    'db':'nuccore',
    'report':'gene_fasta',
    'id' : ",".join(IDs)
  }
  response = requests.get(ncbi_url,params=params)
  print("fetch:", name)
  with open(f"{name}.txt","w") as f:
    f.write(response.text)

# read xlsx
import pandas as pd
path = "NCBI-test.xlsx" #file (xlsx) path
df = pd.read_excel(path)
pbar = tqdm(total=len(df),desc="Fetching data...")
for i in range(len(df)):
  name=""
  Accessions = []
  for j in range(len(df.iloc[i])):
    if j == 0:
      name = df.iloc[i,j]
    else:
      Accessions.append(df.iloc[i,j])
  fetch_data(name,Accessions)
  pbar.update(1)
