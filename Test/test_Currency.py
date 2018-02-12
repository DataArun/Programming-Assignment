
import os
os.getcwd()
from Currency import app 
import unittest
#create Class to test
class FlaskTests(unittest.TestCase): 
# initisalise the app
    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True 
        
# check for home page        
    def test_home_status_code(self):
        result = self.app.get('/') 
        self.assertEqual(result.status_code, 404) 
# Task 1 Success
    def test_task1Sucess(self):
        DateRange = "2017-01-02"
        result = self.app.get('/Date/' +DateRange ) 
        self.assertEqual(result.status_code, 200) 
# Task 1 if entered wrong date
    def test_task1_FailureDate(self):
        DateRange = "2017sd-01-02"
        result = self.app.get('/Date/' +DateRange ) 
        self.assertEqual(result.data, b'{"Message": "Incorrect data format, should be YYYY-MM-DD"}') 

# Task 2 success
    def test_task2Sucess(self):
        DateRange = "2012-12-01"
        currencyA = "SGD"
        currencyB = "EUR"
        result = self.app.get('/CurrencyRange/'+DateRange+ '/'+currencyA +'/'+currencyB) 
        self.assertEqual(result.status_code, 200) 
# Task 2 giving a wrong date
    def test_task2_FailureDate(self):
        DateRange = "20dfg12-12-01"
        currencyA = "SGD"
        currencyB = "EUR"
        result = self.app.get('/CurrencyRange/'+DateRange+ '/'+currencyA +'/'+currencyB) 
        self.assertEqual(result.data, b'{"Message": "Incorrect data format, should be YYYY-MM-DD"}') 
# Task 2 giving a currecny not in the list
    def test_task2_FailureCurrencyNotinList(self):
        DateRange = "2012-12-01"
        currencyA = "SdfvdfgGD"
        currencyB = "EUR"
        result = self.app.get('/CurrencyRange/'+DateRange+ '/'+currencyA +'/'+currencyB) 
        self.assertEqual(result.status_code, 200) 
# Task 2 giving a currecny with wrong spelling 
    def test_task2_FailureCurrencyWrongSpelling(self):
        DateRange = "20dfg12-12-01"
        currencyA = "SGD"
        currencyB = "EURO"
        result = self.app.get('/CurrencyRange/'+DateRange+ '/'+currencyA +'/'+currencyB) 
        self.assertEqual(result.status_code, 200) 
#      
# Task 3 success story
    def test_task3Sucess(self):
        DateRangeA = "2012-12-01"
        DateRangeB = "2018-12-01"
        currencyA = "SGD"
        result = self.app.get('/Daterange/'+DateRangeA+ '/'+DateRangeB +'/'+currencyA) 
        self.assertEqual(result.status_code, 200) 
# Task 3 if wrong date format is given
    def test_task3_FailureDate(self):
        DateRangeA = "2012234234234-12-01"
        DateRangeB = "2018-12-01"
        currencyA = "SGD"
        result = self.app.get('/Daterange/'+DateRangeA+ '/'+DateRangeB +'/'+currencyA) 
        self.assertEqual(result.status_code, 200) 
# Task 3 if currency not in list given
    def test_task3_FailureCurrencyNotinList(self):
        DateRangeA = "2012-12-01"
        DateRangeB = "2018-12-01"
        currencyA = "SGsfsdfsdfD"
        result = self.app.get('/Daterange/'+DateRangeA+ '/'+DateRangeB +'/'+currencyA) 
        self.assertEqual(result.status_code, 200) 
# Task 3 if currency with wrong spelling
    def test_task3_FailureCurrencyWrongSpelling(self):
        DateRangeA = "2012-12-01"
        DateRangeB = "2018-12-01"
        currencyA = "EURO"
        result = self.app.get('/Daterange/'+DateRangeA+ '/'+DateRangeB +'/'+currencyA) 
        self.assertEqual(result.status_code, 200) 
        



if __name__ == "__main__":
    unittest.main()
