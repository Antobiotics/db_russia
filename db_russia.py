#!/usr/local/bin/python
# coding: KOI8-R

from BeautifulSoup import BeautifulSoup
import os,sys
import re

##LAST PROBLEM: WHAT IS nbsp ?
#FILLING MATRIX
# MATRIX -> CSV

def point2vir(flo):
	st = str(flo)
	ind = 0
	for i in range(0,len(st)):
		if(st[i]=='.'):
			ind = i		
			break
	res = st[0:(ind)]+','+st[(ind+1):len(st)]
	return res


def getOKATO(path):
	file_path = path + "/index.html"
	city = open(file_path)
	rea = city.read()
	exp  = re.compile(r"OKATO.(\d+)",re.X)
	tt = exp.findall(rea)
	return tt[0]

def getCoord(path):
	file_path = path+"/index.html"
	city = open(file_path)
	rea = city.read()
	exp = re.compile(r"(\d+).deg.(\d+)",re.U)
	tt = exp.findall(rea)
#	print tt
	first1 = tt[0]
	conv1 = float(first1[1])/60
	res1 = float(first1[0])+conv1
	st1 =point2vir(res1)
	first2 = tt[1]
	conv2 = float(first2[1])/60
	res2 = float(first2[0])+conv2
	st2 = point2vir(res2)
	print str(res1)+" "+str(res2) 
	print st1+" "+st2
	res_ar = [st1,st2]
#	print res_ar

	exp_r = re.compile(r"\s(\d+)\<",re.U)
	tt_r = exp_r.findall(rea)
#	print tt_r
	res3 = tt_r[0]
#	print res3
	res_ar.append(res3)
	return res_ar
	#soup = BeautifulSoup(rea)
	#aa = soup.prettify()
	#print aa[0]
	#text_parts = soup.findAll('br')
	#print text_parts

#path_test ="/Users/gregoirelejay/tt/www.mojgorod.ru/kirovsk_obl/luza"
def parse_and_fill(path):
	file_path = path + "/index.html"
	city = open(file_path)
	rea = city.read()
	soup = BeautifulSoup(rea)
	text_parts = soup.findAll('table')
	table = text_parts[len(text_parts)-2]
#	print(len(text_parts))
#	print(text_parts[len(text_parts)-2])
	pile = []
	for row in table.findAll('tr')[1:]:
		cols = row.findAll('td')
	#	print(cols)
		for col in cols:
			#print(type(str(col)))
		#	print(str(col))
			if(col.find("b")):
				exp = re.compile(r"\w*")
				date = exp.findall(str(col))
				value = date[6]
				pile.append(value)
			#	print value
			else:
				exp = re.compile(r"\w*")
				num = exp.findall(str(col))
				#print num
			#value = num[3]+num[4]+num[5]
				if(not(num[3]=='' and num[5]=='')):
					value = num[3]+","+num[5]
			#		print value
					pile.append(value)
#Make array of (year,values):
	#print(pile)
	#print len(pile)
	i = 0 
	ar = []
	for va in pile:
		if((i%2 == 0 and (not i==0)) and (not ((i+1)==len(pile)))):
			el = (int(pile[i-2]),pile[i-1])
			ar.append(el)
		#	print(el)
		if((i%2 == 0) and ((i+2)==len(pile))):
		#	print "here"
			el = (int(pile[i]),pile[i+1])
			ar.append(el)
		#	print el
		i = i + 1
	#print len(ar)						
	return ar

def getcol(val,matrix):
	res = []
	for i in range(len(matrix)):
		t= matrix[i]
		res.append(t[val])
	return res

def suppress_empty_c(matrix,col_n):
	res = []
	for col in range(col_n):
		colu = getcol(col,matrix)
		bool = 0
		for elem in colu:
			if(elem != ""):
				bool = 1
		if(bool == 0):
			res.append(colu) 	
	return res

if __name__ == '__main__':


	#INITIALIZE:
#	csv_v = [[ 0 for i in range(2010-1765+2)] for j in range(1101)]
	csv_v = [[ "" for i in range(2010-1765+5)] for j in range(1101)]

	csv_v[0][0] ="ville"
	csv_v[0][1] = "OKATO"
	csv_v[0][2] = "l1"
	csv_v[0][3] = "l2"
	csv_v[0][4] = "l3"
	for j in range(5,2010-1765+2):
		csv_v[0][j] = 1765+j-1
	#TRAVELLING:
	path_base ="/Users/gregoirelejay/tt/files/"
	pro_dir = os.listdir(path_base)
#	print pro_dir
	os.chdir(path_base)
	#CITY INDEX:
	index = 1
#	print pro_dir
	for pro in pro_dir:
		if os.path.isdir(pro) == True:
			os.chdir(path_base+pro)
			cities  = os.listdir('.')
#			print cities
			for city in cities:
				if os.path.isdir(city) == True:
					os.chdir(os.path.curdir+"/"+city)
					#PROCESSING:
					#print os.listdir('.')
					print city
					ar =parse_and_fill(os.curdir)
					#FILL MAIN MATRIX:
					csv_v[index][0] = city
					#OKATO STYLE !!!
					csv_v[index][1] = getOKATO(os.curdir)
					coor = getCoord(os.curdir)
					csv_v[index][2] = coor[0]
					csv_v[index][3] = coor[1]
					csv_v[index][4] = coor[2]
					for (d,v) in ar:
						csv_v[index][d-1765+1]=v
					#print ar
					index = index + 1
				#	print "------"
					os.chdir("..")
			os.chdir("..")
#	print index
#	print csv_v
#	csv_v = suppress_empty_c(csv_v,2010-1765+2)
#MAKE CSV FILE FROM MAIN MATRIX:
	c_path = path_base+"russia.csv"
	ci = open(c_path,"w")
	#MAKE CSV HEADER:
	for j in range(2010-1765+2):
		if(j<2010-1765+1):
			ci.write(str(csv_v[0][j])+'\t')
		else:
			ci.write(str(csv_v[0][j])+'\n')
	#FILL THE REST:	
	for i in range(1,1101):
		for j in range(2010-1765+2):
			
			if(j<2010-1765+1):
				ci.write(str(csv_v[i][j])+'\t')
			else:
				ci.write(str(csv_v[i][j])+'\n')



	ci.close()


#parse_and_fill("/Users/gregoirelejay/tt/files/altajsk_kraj/alejsk")
#parse_and_fill("/Users/gregoirelejay/tt/files/jaroslav_obl/rostov")
