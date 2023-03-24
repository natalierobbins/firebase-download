def confirm_files(selected):
  print("\n---------\nBelow are the selected files for download. If you would like to change your files, run this code block again before downloading.\n")
  for blob in selected:
    print(blob.name)

def select_files():
  app = firebase_admin.get_app(name)
  blobs = list(storage.bucket(app=app).list_blobs())
  root_dirs = set()
  nav = []

  depth = 0

  for blob in blobs:
    split = blob.name.split('/')
    root_dirs.add(split[0])

  dir_dict = {}
  print(f"""List of folders/files at depth {depth}:""")
  for i, dir in enumerate(sorted(root_dirs)):
    print(f"""[{i + 1}]""", dir)
    dir_dict[i + 1] = dir
  print("Input the number associated with the desired folder/file for download, or input 'all' to select all:\n")
  selected = input().strip()
  print("\n---------\n")

  done = False
  while not done:
    selected_dirs = set()
    if selected == "all":
        for blob in blobs:
          if blob.name.split('/')[:depth] == nav:
            if blob.name.split('/')[depth]:
              selected_dirs.add(blob.name.split('/')[depth])
        done = True
    else:
      try:
        nav.append(dir_dict[int(selected)])
        depth += 1
        for blob in blobs:
          if blob.name.split('/')[:depth] == nav:
            if blob.name.split('/')[depth]:
              selected_dirs.add(blob.name.split('/')[depth])
        print(f"""List of directories at depth {depth}:""")
        for i, dir in enumerate(sorted(selected_dirs)):
          print(f"""[{i + 1}]""", dir)
          dir_dict[i + 1] = dir
        print("Input the number associated with the desired folder/file for download, or input 'all' to select all:\n")
        selected = input().strip()
        print("\n---------\n")
      except:
        print("Please input a valid number or 'all'")
        selected = input().strip()

  selected_blobs = []
  for dir in selected_dirs:
    navCopy = [x for x in nav]
    navCopy.append(dir)
    for blob in blobs:
      if blob.name.split('/')[:len(navCopy)] == navCopy:
        selected_blobs.append(blob)

  return selected_blobs

def firebase_download(selected_blobs, data_directory):
  failed = []
  print("Note that it may take a few seconds for the downloaded files to upload to your Google Drive\n")
  for blob in tqdm(list(selected_blobs), desc="Downloading files..."):
    filename = blob.name.split('/')[-1]
    target_directory = f"""{data_directory}{'/'.join(blob.name.split('/')[:-1])}/"""
    blob.make_public()
    response = requests.get(blob.public_url).content
    os.makedirs(target_directory, exist_ok=True)
    try:
      with open(f"""{target_directory}{filename}""", 'w') as f:
        f.write(response.decode())
    except:
      failed.append(f"""{target_directory}{filename}""")
  print('\n')
  for failure in failed:
    print(f"""!!! Unable to download: {failure}""")
