from django.shortcuts import render
from django.http import HttpResponse
import csv
from basics.models import Historical_stock_prices
from basics.models import Recently_Updated_Records, All_Records_Table, Logs
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import DataSerializer, UpdatedDataSerializer, HistoryDataSerializer
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.views import APIView
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
# no of days between two dates
def dateDifference(date1, date2):
    date1 = date1.replace("-","/")
    date2 = date2.replace("-","/")
    print("date1")
    print(date1)
    date1 = datetime.strptime(date1, "%d/%b/%y")
    print("date updated")
    print(date1)
    date2 = datetime.strptime(date2, "%d/%b/%y")
    print(date2)
    ("date difference")
    print((date2 - date1).days)
    return (date2 - date1).days
def saveToHistory(updates):
    print("inhistory")
    rec = Historical_stock_prices()
    rec.stock_name = updates.stock_name
    rec.trading_date = updates.trading_date
    rec.closing_price = updates.closing_price
    rec.price_difference = updates.price_difference
    rec.up_or_down_circuit_indicator = updates.up_or_down_circuit_indicator
    rec.upper_price_circuit = updates.upper_price_circuit
    rec.lower_price_circuit = updates.lower_price_circuit
    rec.no_of_falls = updates.no_of_falls
    rec.no_of_rises = updates.no_of_falls
    rec.no_of_days_since_last_circuit = updates.no_of_days_since_last_circuit
    rec.save()
def saveToRecords(updates):
    rec = All_Records_Table()
    rec.stock_name = updates.stock_name
    rec.trading_date = updates.trading_date
    rec.closing_price = updates.closing_price
    rec.price_difference = updates.price_difference
    rec.up_or_down_circuit_indicator = updates.up_or_down_circuit_indicator
    rec.upper_price_circuit = updates.upper_price_circuit
    rec.lower_price_circuit = updates.lower_price_circuit
    rec.no_of_falls = updates.no_of_falls
    rec.no_of_rises = updates.no_of_falls
    rec.no_of_days_since_last_circuit = updates.no_of_days_since_last_circuit
    rec.save()
# handles api call data
def is_update_required(recievedValue): 
    print("inside is update required")
    
    try:
        updatedRec =Recently_Updated_Records.objects.get(stock_name=recievedValue['stock_name'])
        print("record exists")
        previous_no_of_rises = updatedRec.no_of_rises
        previous_no_of_falls = updatedRec.no_of_falls
        previous_Upper_Circuit = updatedRec.upper_price_circuit
        previous_Lower_Circuit =  updatedRec.lower_price_circuit
        previous_trading_date = updatedRec.trading_date

    # lowercircuit
        if(recievedValue['closing_price']< updatedRec.lower_price_circuit):        
            for i in recievedValue:
                if i=='stock_name':
                    updatedRec.stock_name = recievedValue[i]
                if i=='trading_date':
                    updatedRec.trading_date = recievedValue[i]
                if i=='closing_price':
                    updatedRec.closing_price = recievedValue[i]
                updatedRec.price_difference = float(updatedRec.closing_price) * 0.05
                updatedRec.upper_price_circuit = float(updatedRec.closing_price) * 1.05
                updatedRec.lower_price_circuit = float(updatedRec.closing_price)* 0.95
                updatedRec.no_of_falls = previous_no_of_falls + 1
                updatedRec.no_of_rises = updatedRec.no_of_rises
                updatedRec.no_of_days_since_last_circuit = dateDifference(previous_trading_date, updatedRec.trading_date )
                updatedRec.up_or_down_circuit_indicator ='Down'
                saveToHistory(updatedRec)
                saveToRecords(updatedRec)
                updatedRec.save()
            #  upper circuit
        elif(recievedValue['closing_price']> updatedRec.upper_price_circuit):
            for i in recievedValue:
                if i=='stock_name':
                    updatedRec.stock_name = recievedValue[i]
                if i=='trading_date':
                    updatedRec.trading_date = recievedValue[i]
                if i=='closing_price':
                    updatedRec.closing_price = recievedValue[i]
            updatedRec.price_difference = float(updatedRec.closing_price) * 0.05
            updatedRec.upper_price_circuit = float(updatedRec.closing_price) * 1.05
            updatedRec.lower_price_circuit = float(updatedRec.closing_price)* 0.95
            updatedRec.no_of_falls = previous_no_of_falls 
            updatedRec.no_of_rises = (updatedRec.no_of_rises) + 1
            updatedRec.no_of_days_since_last_circuit = dateDifference(previous_trading_date, updatedRec.trading_date )
            updatedRec.up_or_down_circuit_indicator ='Up'
            saveToHistory(updatedRec)
            saveToRecords(updatedRec)
            updatedRec.save() 
            
        
        else:
            dummyData = All_Records_Table()
            dummyData.stock_name = recievedValue['stock_name']
            dummyData.trading_date = recievedValue['trading_date']
            dummyData.closing_price = recievedValue['closing_price']
            dummyData.no_of_rises = updatedRec.no_of_rises
            dummyData.no_of_falls = updatedRec.no_of_falls
            dummyData.price_difference = " "
            dummyData.no_of_days_since_last_circuit= updatedRec.no_of_days_since_last_circuit
            dummyData.lower_price_circuit =""
            dummyData.upper_price_circuit=""
            dummyData.up_or_down_circuit_indicator = ""
            dummyData.save()  
        print("update done")
    except Recently_Updated_Records.DoesNotExist:
        print("not exists")
        newLog = Logs()
        # make entry in log file
        newLog.Action =str("Scrip Name" +" "+ recievedValue['stock_name']+ " "+"not present")
        newLog.save()
        updatedRec = Recently_Updated_Records()
        rec = Historical_stock_prices()
        dummyData = All_Records_Table()
        updatedRec.stock_name = recievedValue['stock_name']
        updatedRec.closing_price = recievedValue['closing_price']
        updatedRec.trading_date = recievedValue['trading_date']        
        updatedRec.price_difference = float(updatedRec.closing_price) * 0.05
        updatedRec.upper_price_circuit = float(updatedRec.closing_price) * 1.05
        updatedRec.lower_price_circuit = float(updatedRec.closing_price)* 0.95
        updatedRec.no_of_falls = 0
        updatedRec.no_of_rises = 0
        updatedRec.no_of_days_since_last_circuit=0
        updatedRec.up_or_down_circuit_indicator =''
       
        saveToHistory(updatedRec)
        saveToRecords(updatedRec)
        updatedRec.save()
       
   
        
# entry to recently updated table based on downloaded historical_price_sheet of every scrip
def TrackUpdates(rec):
    updatedRec =Recently_Updated_Records()
    updatedRec.stock_name= rec.stock_name
    updatedRec.trading_date = rec.trading_date
    updatedRec.closing_price =rec.closing_price
    updatedRec.price_difference=rec.price_difference    
    updatedRec.upper_price_circuit = rec.upper_price_circuit
    updatedRec.lower_price_circuit = rec.lower_price_circuit
    updatedRec.no_of_days_since_last_circuit = rec.no_of_days_since_last_circuit
    updatedRec.up_or_down_circuit_indicator = rec.up_or_down_circuit_indicator
    updatedRec.no_of_rises = rec.no_of_rises
    updatedRec.no_of_falls = rec.no_of_falls
    updatedRec.save()

# make entry to dummy table
def addRecordsToAll_Records_Table(rec):
    dummyData = All_Records_Table()
    dummyData.stock_name = rec.stock_name
    dummyData.trading_date = rec.trading_date
    dummyData.closing_price = rec.closing_price
    dummyData.price_difference=rec.price_difference
    dummyData.lower_price_circuit= rec.lower_price_circuit
    dummyData.upper_price_circuit = rec.upper_price_circuit
    dummyData.no_of_falls = rec.no_of_falls
    dummyData.no_of_rises = rec.no_of_rises
    dummyData.no_of_days_since_last_circuit = rec.no_of_days_since_last_circuit
    dummyData.save()

# evaluate historicat_prices_sheet of every scrip
def index(request):
    with open ('dmartNew.csv', 'r') as f:
        reader = csv.reader(f)
        entries=[]
        priceUpRecord=[]
        priceDownRecord=[]
        dateRecords=[]
        cnt=1
        nUps=0
        nDowns=0
        for i, row in enumerate(reader):
            isScripRecordPresent =Recently_Updated_Records.objects.filter(stock_name=row[0])[:1]
        #  ignore title of column   
            if (i==0):
                print("wrong")
                pass
            elif(i==1):
                
                rec = Historical_stock_prices()
                print(len(isScripRecordPresent))
                row = " ".join(row)
                row = row.replace(";"," ")
                row= row.split()
                rec.stock_name =row[0]
                print("close" + row[2])
                rec.trading_date = row[2]
                rec.closing_price= row[8]
                addRecordsToAll_Records_Table(rec)
                rec.price_difference =float(row[8])*0.05
                rec.upper_price_circuit =   (float(row[8])*0.05) +   float(row[8])
                rec.lower_price_circuit =  float(row[8])-(float(row[8])*0.05)   
                rec.no_of_days_since_last_circuit= 0
                rec.up_or_down_circuit_indicator='nil'
                priceUpRecord.insert(0,float(rec.upper_price_circuit))
                priceDownRecord.insert(0,rec.lower_price_circuit)
                rec.no_of_rises=0
                rec.no_of_falls=0
                entries.append(rec)
                dateRecords.insert(0,rec.trading_date)
                print("executed")
                rec.save()
                if(len(isScripRecordPresent) == 0):
                    TrackUpdates(rec)
                pass
            else:
                cnt+=1
                rec = Historical_stock_prices()
                row = " ".join(row)
                row = row.replace(";"," ")
                row= row.split(" ")
                rec.stock_name = row[0]
                rec.trading_date = row[2]
                rec.closing_price= row[8]
                print("closingprice" + rec.closing_price)
                print(priceUpRecord[0])
# checking for lower price
                if(float(rec.closing_price) > float(priceUpRecord[0])):
                    rec.price_difference =float(row[8])*0.05
                    rec.upper_price_circuit =   (float(row[8])*0.05) +   float(row[8])
                    priceUpRecord.insert(0,rec.upper_price_circuit)
                    rec.lower_price_circuit = float(row[8])- (float(row[8])*0.05) 
                    priceDownRecord.insert(0,rec.lower_price_circuit)
                    nUps +=1
                    
                    rec.no_of_days_since_last_circuit = dateDifference(dateRecords[0], rec.trading_date)
                    dateRecords.insert(0,rec.trading_date)
                    rec.up_or_down_circuit_indicator ='Up'
                    rec.no_of_rises = nUps
                    rec.no_of_falls = nDowns
                    addRecordsToAll_Records_Table(rec)
                    rec.save()
                    if(len(isScripRecordPresent) != 0):
                        TrackUpdates(rec)
# checking for upper price   
                elif(float(rec.closing_price) < float(priceDownRecord[0])):
                    rec.price_difference =float(row[8])*0.05
                    rec.lower_price_circuit = float(row[8])- (float(row[8])*0.05) 
                    priceDownRecord.insert(0,rec.lower_price_circuit)
                    rec.upper_price_circuit =   (float(row[8])*0.05) +   float(row[8])
                    priceUpRecord.insert(0,rec.upper_price_circuit)
                   
                    rec.no_of_days_since_last_circuit= dateDifference(dateRecords[0], rec.trading_date)
                    dateRecords.insert(0,rec.trading_date)
                    nDowns +=1
                    rec.up_or_down_circuit_indicator ='Down'
                    rec.no_of_rises = nUps
                    rec.no_of_falls = nDowns
                    addRecordsToAll_Records_Table(rec)
                    rec.save()
                    if(len(isScripRecordPresent) != 0):
                        TrackUpdates(rec)
                else:
                    
                    rec.price_difference =" "
                    rec.lower_price_circuit =   " "
                    rec.upper_price_circuit=" "
                    rec.no_of_days_since_last_circuit=""
                    rec.no_of_falls = nDowns
                    rec.no_of_rises = nUps

                    # rec.save()
                    addRecordsToAll_Records_Table(rec)
                entries.append(rec)
    return HttpResponse('<h1>basics</h1>')

# Handling restapi calls

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def check_if_update_present(request):
    if request.method == 'POST':
    
        data = JSONParser().parse(request)
        serializer =DataSerializer(data=data)
        if serializer.is_valid():
            is_update_required(serializer.data)
            return JsonResponse(serializer.data, status=201)
          
        return HttpResponse('<h1>sucess</h1>')

# get call for recect updated data of each scrip
# @csrf_exempt 
class check_recent_record(APIView):
    def get_object(self, stock_name):
        try:
            return Recently_Updated_Records.objects.get(stock_name=stock_name)
        except Recently_Updated_Records.DoesNotExist:
            raise Http404
    def get(self, request, stock_name, format= None): 
        snippet = self.get_object(stock_name)
        serializer = UpdatedDataSerializer(snippet)
        return Response(serializer.data)
        
#api for historical data of eact scrip
# @csrf_exempt 
class check_historical_record(APIView):
    def get_object(self, stock_name):
        try:
            return Historical_stock_prices.objects.filter(stock_name=stock_name)
        except Recently_Updated_Records.DoesNotExist:
            raise Http404 
    def get(self, request, stock_name, format= None): 
        snippet = self.get_object(stock_name)
        serializer = HistoryDataSerializer(snippet, many= True)
        return Response(serializer.data) 