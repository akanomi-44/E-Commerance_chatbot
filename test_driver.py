import db_helper as db 

class Test():
    def __init__(self):
        self.passCase = 0
        self.failCase = 0
    
    def print(self):
        print("==============================")
        print(f"pass case: {self.passCase}")
        print(f"fail case: {self.failCase}")
        print(f"Avg: {self.passCase / (self.passCase + self.failCase)}")
        print("==============================")

    def evaluate(self,func, input, expectedResult):
        actualResult:str = func(input)
        print(f"\t expectedResult: {expectedResult}, \n \t actualResult: {actualResult}")
        print(f"-------------------------------------------------------------------------------------------")
        if actualResult == expectedResult:
            self.passCase += 1;
        else:
            self.failCase += 1;
    
    def inputRead(self,name):
        self.inputData = []
        with open(name, "r") as open_file:
            self.inputData = open_file.read().splitlines()

if __name__ == "__main__":
    cusReq = db.Server(dbName="Store",collectionName="cusReq")
    template = db.Server(dbName="Store",collectionName="templateReq")
    cusReq.embField = 'req'
    template.embField = 'req'
    
    tester = Test()
    df = cusReq.toDF()    
    
    for i,item in df.iterrows():
        print(f"case: {item['req']}")
        tester.evaluate(template.getMostRelavantVec,item['embedding'],item['case_no'])
        print("###########################################################################################\n")


    print(f"**Test report**")
    tester.print()
