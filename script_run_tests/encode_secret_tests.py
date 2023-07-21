import hashlib, argparse

def encode_test_md5(path_file):
  with open(path_file, 'r') as file:
    lines = file.readlines()
  new_list = [i.strip() for i in lines]
  str_list = "\n".join(new_list)
  hash_md5 = hashlib.md5(str_list.encode()).hexdigest()
  return hash_md5

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-p', '--path', required=True)
  args = parser.parse_args()
  print(encode_test_md5(args.path))


