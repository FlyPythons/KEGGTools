# KEGGTools
A collection of tools to download and process KEGG database
## Introduction
KEGG is an important database to research on the function of proteins and metabolic pathways of certain organism, but the sequences in KEGG databases can not be downloaded free. KEGGTools is developed to solve this problem.
### Requirements
* Python 3.5+
### Install
to git  
```
git clone https://github.com/FlyPythons/KEGGTools.git
```
or download
```
wget https://github.com/FlyPythons/KEGGTools/archive/master.zip
unzip mater.zip
```
## Examples
### Download KEGG database
1. Download information of KEGG organisms from KEGG   
```
python3 download_organism.py --url http://www.kegg.jp/kegg/catalog/org_list.html --out KEGG.org
```
This will get 5426 KEGG organisms from KEGG-Genome.  

2. Download protein sequences from NCBI by the urls in 'KEGG.org'
```
python3 download_proteins --org KEGG.org -out NCBI-proteins --concurrent 2
```
This will get 5419 gzip formatted protein sequences of KEGG organisms from NCBI. Other 7 organsims are not from NCBI, they are "bpg dosa lem lja pfd pfh smin"  
3. Download KO information from KEGG
```
python3 download_ko.py --org KEGG.org --out KEGG-KO --concurrent 10
```
This will get 5394 keg formatted file consist KO information of KEGG organisms. Other 32 organisms have no KO information in KEGG, they are "ebc pcd apor pgz vta cola haf mii aea nmj bgm aon kso zpa afq amih ypac mee msao dpc rhq dlu cgrn sfk actt pbf kst vbh fmo ful pbp dod "  
4. Get proteins included in KO files from NCBI download proteins  
```
python3 process_proteins.py --org KEGG.org --keg KEGG-KO --pep NCBI-proteins --out KO-proteins
```
This will get protein sequences of 5381 organisms. 13 of organsims can not find matched id in KEGG-KO and NCBI-protein, they are "agl cpor pary smiz pshi tng vrm dpl dco hlc ecor nwe xph"; 32 organisms have no KO information in KEGG, they are present in step 4.  
So finally, we have a KEGG database consist 5381 organisms, we can use them to do KEGG annotation. 
### Process KEGG database downloaded
* Get the NCBI Taxonomy ranks of KEGG organisms
```
python3 get_ranks.py --keg br08610.keg --taxon taxonomy.ranks --out KEGG.ranks
```
This will find 4715 Bacteria, 442 Eukaryota, 269 Archaea in KEGG organisms.
* Extract the information of KEGG organisms you wanted to make db
```
python3 makedb.py --org human.org --keg KEGG-KO --pep NCBI-proteins --out human
```
This will create 2 files consist of protein fasta file("human.pep.fasta") and protein related KO and pathway ID("human.pep2ko.txt").
### Plot KEGG annotation result
make kegg annotaion result like "human.pep2ko.txt"  
* Create KEGG pathway file ".keg"
```
python3 make_keg.py --keg ko00001.keg --in human.pep2ko.txt --out human
```
This will create a keg file named "human.keg"
* Plot KEGG pathway file
```
python3 plot_key.py --keg human.keg --out human
```
This will create a pdf file named "human.pdf"  
![image](https://github.com/FlyPythons/KEGGTools/raw/master/examples/human.png)