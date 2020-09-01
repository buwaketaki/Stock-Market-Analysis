from django.db import models

class Historical_stock_prices(models.Model):
    stock_name=  models.CharField(max_length=200, blank=True)
    trading_date= models.CharField(max_length=200)
    closing_price= models.CharField(max_length=200)
    price_difference = models.CharField(max_length=100, blank=True)
    lower_price_circuit = models.CharField(max_length=200 ,blank=True)
    upper_price_circuit = models.CharField(max_length=200 ,blank=True)
    no_of_days_since_last_circuit = models.CharField(max_length=200 ,blank=True)
    up_or_down_circuit_indicator = models.CharField(max_length=200 ,blank=True)

    no_of_rises = models.IntegerField(blank=True, default=0)
    no_of_falls= models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.Name

class Recently_Updated_Records(models.Model):
    stock_name= models.CharField(max_length=200, blank=True, primary_key=True)
    trading_date= models.CharField(max_length=100, blank=True)
    closing_price= models.CharField(max_length=200, blank=True)
    price_difference = models.CharField(max_length=100, blank=True)
    upper_price_circuit = models.CharField(max_length=200 ,blank=True)
    lower_price_circuit = models.CharField(max_length=200 ,blank=True)    
    up_or_down_circuit_indicator = models.CharField(max_length=200 ,blank=True)
    no_of_days_since_last_circuit = models.CharField(max_length=200 ,blank=True)
    up_or_down_circuit_indicator = models.CharField(max_length=200 ,blank=True)
    no_of_rises = models.IntegerField(blank=True, default=0)
    no_of_falls= models.IntegerField(blank=True, default=0)
  

class All_Records_Table(models.Model):
    stock_name=  models.CharField(max_length=200, blank=True)
    trading_date= models.CharField(max_length=200)
    closing_price= models.CharField(max_length=200)
    price_difference = models.CharField(max_length=100, blank=True)
    lower_price_circuit = models.CharField(max_length=200 ,blank=True)
    upper_price_circuit = models.CharField(max_length=200 ,blank=True)
    no_of_days_since_last_circuit = models.CharField(max_length=200 ,blank=True)
    up_or_down_circuit_indicator = models.CharField(max_length=200 ,blank=True)

    no_of_rises = models.IntegerField(blank=True, default=0)
    no_of_falls= models.IntegerField(blank=True, default=0)

class Logs(models.Model):
    Date = models.DateTimeField(max_length=100,auto_now_add=True )
    Action = models.CharField(max_length=100)