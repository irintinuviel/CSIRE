#wygenerowac zbior PPE, kazdy ppe ma atrybuty: kod ppe (gs1), taryfa( losowo wybrana z grupy dostepnych w standardowych profilach), lista produktow energetycznych wg excela
#tyle ile liczebnosc wygenerowac punktow, taryfa losowo wybrana, tabela 4elementowa: klasa profil liczebnosc, tablica produktow energetycznych
import math
import random
import time
import openpyxl
import csv
from readExcel import getSheets

file = ".\\Klasy-PP.xlsx"

def czytaj_arkusz(plik):
    wb = openpyxl.load_workbook(plik, data_only=True)
    sheet = wb.active
    data = []
    finaldata= []
    for row in sheet.iter_rows(min_row=1, max_row=34,min_col=1, max_col=7):
        data.append([cell.value for cell in row])

    count = 0
    for i in range(1,7):
        finaldata.append([data[0][i]])
        finaldata[count].append(data[1][i])
        finaldata[count].append(data[2][i])
        finaldata[count].append([])
        for j in range(3,len(data)):
            if data[j][i] is not None:
                finaldata[count][3].append(data[j][0])
        count+=1

    return finaldata

def generateData():
    filename = "generatedPPE.csv"
    data = czytaj_arkusz(file)
    sheets = getSheets()
    count = 0
    for row in data:
        n = row[0]
        taryfy = []
        last = 1234567890
        #do pliku
        for k in sheets.keys():
            if k.startswith(row[2]):
                taryfy.append(k)

        for i in range(0,n):
            rand = random.randint(0, len(taryfy) - 1)
            gs1 = generateGS1(last)
            last= gs1[0]
            products = ""
            for e in row[3]:
                products += e+":"
            products= products.rstrip(":")
            with open(filename, 'a',newline="\n") as csvfile:
                s= gs1[1]+ "," +taryfy[rand]+ "," +row[1]+ "," +products+"\n"
                csvfile.write(s)
            count+= 1

def controlSum(code):

    multiplied= []
    sum = 0
    for i in range(0, len(code)):
        e= int(code[i])
        if i%2 == 0:
            multiplied.append(e*3)
        else:
            multiplied.append(e)
    for e in multiplied:
        sum+= e

    closest= math.ceil(sum/10)*10
    return closest-sum

def generateGS1(last):
    KRAJ= "590"
    OSD= "1234"
    number = last+1
    kod = KRAJ+OSD+str(number)
    kontrolna= controlSum(kod)
    kod += str(kontrolna)
    return number,kod


start_time = time.time()
generateData()
print("--- %s seconds ---" % (time.time() - start_time))




