import re

def Read_Two_Column_File(file_name):
    with open(file_name, 'r') as data:
        x = []
        y = []
        for line in data:
            multi_space_split = re.split(r"  ", line)
            #for i, sub_line in enumerate(multi_space_split):
            print(multi_space_split)    
            p = [l for l in multi_space_split if l.replace("\n", "")]
            print(p)
            print(repr(line))
            if not p:
                x.append('\n')
                y.append('\n')
            elif len(p) == 2:
                x.append(p[0])
                y.append(p[1])
            elif len(multi_space_split) > 25:
                y.append(p[0])
            else:
                x.append(p[0])
            x.append('\n')
            y.append('\n')
    return x, y

if __name__ == '__main__':
    x, y = Read_Two_Column_File('text.txt')

    print (' '.join(x)) 
    print (' '.join(y))
