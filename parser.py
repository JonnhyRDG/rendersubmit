class Node():
    def __init__(self):
        self.type_name = None
        self.data = {}
        self.parent = []
        self.child =[]


all = []
root = Node()

all_lines = None
with  open('P:/AndreJukebox/seq/010_NCT/s0130/comp/workfile.nk', 'r') as fil:
    all_lines = fil.readlines()

actual_node = None
for line in all_lines:
    if line.endswith('{\n'):
        actual_node = Node()
        actual_node.type_name = line.split(' ')[0]
    elif line == '}\n' and actual_node:
        all.append(actual_node)
        actual_node = None
    else:
        if not actual_node:
            continue
        if line.startswith(' '):
            line = line[1:]
        attr = line.split(' ')[0]
        val = line.replace("{} ".format(attr), '').replace('\n', '')
        actual_node.data[attr] = val
        # Inter nodo

print([a.data['name'] for a in all if a.type_name == 'Write'])