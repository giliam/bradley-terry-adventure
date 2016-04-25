#!/usr/bin/python
# -*-coding:utf-8 -*

import csv
import random
import math

NUMBER_OF_PAIRS = 136
N = 17
ENABLED_FILE = False
COMPAREASONS_KEY = [(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,9),(0,10),(0,11),(0,12),(0,13),(0,14),(0,15),(0,16),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9),(1,10),(1,11),(1,12),(1,13),(1,14),(1,15),(1,16),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8),(2,9),(2,10),(2,11),(2,12),(2,13),(2,14),(2,15),(2,16),(3,4),(3,5),(3,6),(3,7),(3,8),(3,9),(3,10),(3,11),(3,12),(3,13),(3,14),(3,15),(3,16),(4,5),(4,6),(4,7),(4,8),(4,9),(4,10),(4,11),(4,12),(4,13),(4,14),(4,15),(4,16),(5,6),(5,7),(5,8),(5,9),(5,10),(5,11),(5,12),(5,13),(5,14),(5,15),(5,16),(6,7),(6,8),(6,9),(6,10),(6,11),(6,12),(6,13),(6,14),(6,15),(6,16),(7,8),(7,9),(7,10),(7,11),(7,12),(7,13),(7,14),(7,15),(7,16),(8,9),(8,10),(8,11),(8,12),(8,13),(8,14),(8,15),(8,16),(9,10),(9,11),(9,12),(9,13),(9,14),(9,15),(9,16),(10,11),(10,12),(10,13),(10,14),(10,15),(10,16),(11,12),(11,13),(11,14),(11,15),(11,16),(12,13),(12,14),(12,15),(12,16),(13,14),(13,15),(13,16),(14,15),(14,16),(15,16)]

def generate():
	data = [[]]
	for i in range(150):
		data.append([])
		line = ""
		line += "user" + str(i)
		data[i].append("user" + str(i))
		for j in range(NUMBER_OF_PAIRS):
			b = int(random.random()*100.)%3
			line += ";" + str(b-1)
			data[i].append(b-1)
		print line
	return data

def computeL(wonBy,proba):
	sumL = 0.0
	for i in range(N):
		for j in range(N):
			if proba[i] > 0:
				sumL += wonBy[i][j]*math.log(proba[i]) - wonBy[i][j]*math.log(proba[i]+proba[j])
	return sumL

def computeNewProba(proba,wonBy,numberOfCompareasons):
	newProba = [0.0] * N
	sumNewProba = 0.0
	for i in range(N):
		sumP = 0.0
		for j in range(N):
			if i == j:
				continue
			sumP += numberOfCompareasons[i][j]/(proba[i]+proba[j])

		if sumP == 0:
			newProba[i] = 0.0
		else:
			newProba[i] = wonBy[i]/sumP
		sumNewProba += newProba[i]
	for i in range(N):
		newProba[i] /= sumNewProba
	return newProba

def getData():
	if ENABLED_FILE:
		with open('data.csv', 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=';')
	data = generate()
	return data

def extract():
	data = getData()
	compareasons = [[]] * NUMBER_OF_PAIRS
	omega = [[0.0 for i in range(N)] for j in range(N)]
	wonBy = [0 for i in range(N)]
	duelWonBy = [[0 for i in range(N)] for j in range(N)]
	numberOfCompareasons = [[0 for i in range(N)] for j in range(N)]
	for row in data:
		if len(row) == 0:
			continue
		for j in range(NUMBER_OF_PAIRS):
			compareasons[j].append(row[j+1])
			row[j+1] = float(row[j+1])
			if row[j+1] >= 0:
				omega[COMPAREASONS_KEY[j][0]][COMPAREASONS_KEY[j][1]] += row[j+1]
				omega[COMPAREASONS_KEY[j][1]][COMPAREASONS_KEY[j][0]] += row[j+1]
				if row[j+1] == 1:
					duelWonBy[COMPAREASONS_KEY[j][0]][COMPAREASONS_KEY[j][1]] += 1.
					wonBy[COMPAREASONS_KEY[j][0]] += 1.
				else:
					duelWonBy[COMPAREASONS_KEY[j][1]][COMPAREASONS_KEY[j][0]] += 1.
					wonBy[COMPAREASONS_KEY[j][1]] += 1.
				numberOfCompareasons[COMPAREASONS_KEY[j][0]][COMPAREASONS_KEY[j][1]] += 1
				numberOfCompareasons[COMPAREASONS_KEY[j][1]][COMPAREASONS_KEY[j][0]] += 1

	for j in range(N):
		for i in range(N):
			if numberOfCompareasons[j][i] > 0:
				omega[j][i] /= numberOfCompareasons[j][i]

	proba = [0.5] * N 

	lastL = 0.0
	i = 0
	while i < 10000: 
		i += 1
		proba = computeNewProba(proba, wonBy, numberOfCompareasons)
		newL = computeL(duelWonBy, proba)
		if abs(newL - lastL) < 0.000001:
			print proba
			break
		lastL = newL


def binomiale(n, p):
	denomin = 1
	for i in range(1,n+1):
		denomin *= i

	numer = 1
	for i in range(p-n+1,p+1):
		numer *= i
	return numer/denomin

def create_compareasons_keys():
	out = ""
	k = 0
	for i in range(N):
		for j in range(i,N):
			if i != j and k < NUMBER_OF_PAIRS:
				k+=1
				out += ",(" + str(i) + "," + str(j) + ")"
	print out.strip(",")
	print k

extract()