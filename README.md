# Welcome! 👋
You were probably directed here from my [Firebase/jsPsych tutorial](https://github.com/natalierobbins/firebase-tutorial) for the [CCC Lab](https://sites.google.com/umich.edu/ccc-lab/home) at the University of Michigan. This will be the home of any relevant python scripts you might need during your experiment. Right now, it just includes a script for downloading text files, but I will likely be adding more for downloading audio files and reformatting spreadsheets into .json files. Stay tuned!

If you don't know whether you already have Python with pip installed, you can check by asking for its version in your terminal:
```
python --version
python -m pip --version
```
You will either get the version numbers and/or a file path to where it is on your computer, which means it's already installed, or an error, which means you don't have it installed yet. If that's the case, you can download Python with pip via [their website](https://www.python.org/downloads/).

Please reach out to me at [robbinat@umich.edu](mailto:robbinat@umich.edu) if you have any questions or issues!
## firebase-download.py
### Step 1: Set up your download folder
Decide where you want to keep your downloads from Firebase. The script will automatically make folders in the same layout that they're in in your Firebase storage (so, if you have an EXP_1 folder on Firebase, it will create a EXP_1 folder on your computer with all relevant files). Once you have found or created a destination for your downloads, download the [firebase-download.py](https://github.com/natalierobbins/firebase-download/blob/main/firebase-download.py) script and place it in that folder.
### Step 2: Install required packages
There are two packages this script uses that are not in the Python standard library: [firebase-admin](https://github.com/firebase/firebase-admin-python) and [tqdm](https://tqdm.github.io/). Install them on your terminal.
```
pip install firebase-admin tqdm
```
### Step 3: Download your Firebase credentials
To download your credentials, go to the ```Project Settings``` page of the project you wish to download from on your [Firebase Console](https://console.firebase.google.com/u/0/). Once there, navigate to the ```Service Accounts``` tab.
Click ```Generate new private key```. This will download a ```.json``` file onto your computer that will allow you to read from your Firebase storage. Move this file into the same download destination folder that you chose in Step 1.
### Step 4: Run the script!
Navigate to your download folder in your terminal using ```cd```. For example:
```
cd Users/natalierobbins/path/to/downloads
```
Once there you can run the script:
```
python firebase-download.py
```
There is one command line option: ```--skip``` or ```-s```. Add this to your command if you only wish to download files you haven't downloaded yet. Don't add this if you want to download and possibly overwrite files you've already downloaded in a previous run.
```
python firebase-download.py --skip
```
