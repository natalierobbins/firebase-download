from firebase_admin import storage
from tqdm import tqdm
import requests
import os
from ipytree import Tree, Node
from collections import defaultdict

def traverse(curr_node, filenames):
  # if not leaf node
  if bool(curr_node.nodes):
    for node in curr_node.nodes:
      traverse(node, filenames)
  # leaf node yippee
  else:
    filenames.append(curr_node.name)
    
def get_selected(tree):
  filenames = []
  traverse(tree.selected_nodes[0], filenames)
  return filenames

def firebase_download(app, filenames, data_directory):
  
  blobs = list(storage.bucket(app=app).list_blobs())
  selected_blobs = []
  for blob in blobs:
    if blob.name.split('/')[-1] in filenames:
      selected_blobs.append(blob)
  
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
    
def collapse(curr_node):
  curr_node.opened = False
  for node in curr_node.nodes:
    collapse(node)
    
def build_tree(app):

  tree = Tree(stripes=True, multiple_selection=False)
  blobs = list(storage.bucket(app=app).list_blobs())

  tree.nodes = []

  files = defaultdict(list)
  more_files = defaultdict(list)

  file_tree = []

  file_paths = list(filter(lambda x : x[0][0] != '_' and x[-1] != '', [blob.name.split('/') for blob in blobs]))
  files_at = file_paths

  for file_path in file_paths:
    curr_dir = file_path[:-1]
    curr_file = file_path[-1]
    files['/'.join(curr_dir)].append(Node(curr_file))

  for file_path in files.keys():
    curr_dir = file_path.split('/')[:-1]
    curr_file = file_path.split('/')[-1]
    more_files['/'.join(curr_dir)].append(Node('/'.join(curr_file), files[file_path]))

  for dir in more_files.keys():
    new_node = Node(dir, more_files[dir])
    tree.add_node(new_node)
  
  collapse(tree)
  
  return tree