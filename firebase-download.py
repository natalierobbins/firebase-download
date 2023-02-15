import firebase_admin
import sys
from firebase_admin import credentials, storage
from tqdm import tqdm
import requests
import io
import os
import json
import re

skip = 0
if len(sys.argv) == 2:
    if sys.argv[1] == '--skip' or sys.argv[1] == '-s':
        skip = 1
    else:
        print('Unknown command line argument')
        exit()

# searches for credentials in current directory
def getCredentials():
    files = os.listdir(os.getcwd())
    regex = r'.*firebase-adminsdk.*'
    for file in files:
        match = re.search(regex, file)
        if match:
            return match.group(0)
    return None

# returns storage bucket dict
def getStorageBucket(creds):
    return { 'storageBucket': creds['project_id'] + '.appspot.com' }

# open credentials
try:
    with open(getCredentials(), 'r') as file:
        creds = json.load(file)
except:
    print('Error: could not find Firebase Admin SDK')

# initialization
c = firebase_admin.credentials.Certificate(creds)
s = getStorageBucket(creds)
firebase_admin.initialize_app(c, s)
blobs = storage.bucket().list_blobs()

# gets content from each blob and writes it into directory
for blob in tqdm(list(blobs), desc="Downloading files..."):
    blob.make_public()
    response = requests.get(blob.public_url).content
    if skip and os.path.exists(blob.name):
        pass
    else:
        os.makedirs(os.path.dirname(blob.name), exist_ok=True)
        with open(blob.name, 'w') as f:
            f.write(response.decode())
