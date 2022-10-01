from urllib.request import urlretrieve
import os
def download(url , path):
    try:
        folder = os.path.exists(url , path)
        if not folder:                   
            os.makedirs(path)
        urlretrieve(url , path)
        return True
    except:            
        return False

	
