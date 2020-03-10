import os


directory = './database_COD/'
# make directory database_COD/ if needed
if not os.path.isdir(directory):
    os.mkdir(directory)

file1 = open('COD-selection.txt') 
Lines = file1.readlines() 

print('downloading..')
os.chdir(directory) # change dir to database_COD/
count = 0
for line in Lines[0:3000]:
    # extract url and filename from each line
    url = line[:-1]
    filename = url[35:]
    if os.path.exists(filename) is False:
        import requests
        req = requests.get(url)
        assert req.status_code == 200 # if the download failed, this line will generate an error
        with open(filename, 'wb') as f:
            f.write(req.content)
        count = count + 1
        if count in [10000, 20000, 30000, 40000]:
            print(str(count) + ' downloaded..')

os.chdir('../') # change dir back to default
print(str(count) + ' CIF files downloaded')