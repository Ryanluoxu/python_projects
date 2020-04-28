import sqlite3
import time
import zlib

conn = sqlite3.connect('raw.sqlite')
cur = conn.cursor()


def getMonth(month):
    if month == "Jan": return "01"
    if month == "Feb": return "02"
    if month == "Mar": return "03"
    if month == "Apr": return "04"
    if month == "May": return "05"
    if month == "Jun": return "06"
    if month == "Jul": return "07"
    if month == "Aug": return "08"
    if month == "Sep": return "09"
    if month == "Oct": return "10"
    if month == "Nov": return "11"
    if month == "Dec": return "12"

def getDate(date):
    if date == "1st": return "01"
    if date == "2nd": return "02"
    if date == "3rd": return "03"
    if date == "21st": return "21"
    if date == "22nd": return "22"
    if date == "23rd": return "23"
    if date == "31st": return "31"
    result = date.replace("th","")
    if len(result) < 2: result = "0"+result
    return result

def convertToDate(dateStr):
    # 29th, Jan 2020
    parts = dateStr.split()
    year = parts[2]
    month = getMonth(parts[1])
    date = getDate(parts[0].replace(",",""))
    return year+"-"+month+"-"+date


data = {}
cur.execute('SELECT confirmed_date, nationality FROM cases')
for row in cur :
    date = convertToDate(row[0])
    nationality = row[1]

    if date in data:
        dict = data[date]
        dict[nationality] = dict.get(nationality,0)+1
    else:
        dict = {}
        dict[nationality] = 1
        data[date] = dict


# insert data into js
# nationality:
fhand = open('xline.js','w')
fhand.write("xline = [ ['Date'")
nationalityList = []
cur.execute('SELECT DISTINCT nationality FROM cases')
for row in cur:
    nationalityList.append(row[0])
    fhand.write(",'"+row[0]+"'")
fhand.write("]")


# count for each date
for key in sorted(data.keys()):
    dict = data[key]
    fhand.write(",\n['"+key+"'")
    for nationality in nationalityList:
        val = dict.get(nationality,0)
        fhand.write(","+str(val))
    fhand.write("]");

fhand.write("\n];\n")
fhand.close()

print("Output written to xline.js")
print("Open xline.htm to visualize the data")
