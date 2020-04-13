import objgraph
dict_list = objgraph.by_type('dict')
def save_to_file(self, name, items):
  with open(name, 'w') as outputs:
    for idx, item in enumerate(items):
      try:
        outputs.write(str(idx) + " ### ")
        outputs.write(str(item))
        outputs.write('\n')
      except Exception as e:
        print(e)
    outputs.flush()