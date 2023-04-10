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
        print("Case: ")
        print(f"\tTest: {input}, \n \t expectedResult: {expectedResult}, \n \t actualResult: {actualResult}")
        print(f"-------------------------------------------------------------------------------------------")
        if actualResult == expectedResult:
            self.passCase += 1;
        else:
            self.failCase += 1;

def echo(text):
    return text
if __name__ == "__main__":
    server = db.Server(dbName="Store",collectionName="reqTemplate")
    server.embField = "req"
    test = Test()
    test.evaluate(server.getMostRelavant,"i'm looking for a formal clothing for a weeding", "assist with product selection")
    test.evaluate(server.getMostRelavant,"There are some problems with my order", "make a complaint about the product")
    test.evaluate(server.getMostRelavant,"where can i order it", "place an order")
    test.evaluate(server.getMostRelavant,"is this shirt avalable", "Check product availability")
    test.print()
    
   
