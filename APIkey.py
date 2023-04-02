import os
def get_key():
    if os.path.exists('./APIkey.txt'):
        with open('./APIkey.txt') as f:
            key = f.readline()
            return key
    else:
        raise NameError("Missing API key! Please create APIkey.txt and put the openai API key in it !")
    
if __name__ == "__main__":
    get_key()