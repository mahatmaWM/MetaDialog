
data = {
    'name':
        {'sparise':
             {'citylist':
              ['北京','上海'],
              },
         'mingzi':
             ['suibian','douxing'],
         'nodes':
            ['hah','yehao'],
         },
    'qita':
        {'wual':
             {'zenm':['shuo','eihei']}}
}

def Write_json(path,data):
    with open(path, "w+", encoding="utf-8") as f:
        f.write("[")
        lp = 0
        for p in data['name']:
            if lp > 0:
                f.write(",\n")
            else:
                f.write("\n")
            f.write("{\n")
            f.write('"Code":"%s"\n' % p[1])
            f.write(',"Name":"%s"\n' % p[2])
            f.write(',Nodes:[\n')
            citylist = p[1]['citylist']
            lc = 0
            for c in citylist:
                if lc > 0:
                    f.write("\t,\n")
                else:
                    f.write("\n")
                f.write("\t{\n")
                f.write('\t"Code":"%s"\n' % c[1])
                f.write('\t,"Name":"%s"\n' % c[2])
                f.write('\t,Nodes:[\n')
                arealist = c[1]['arealist']
                la = 0
                for a in arealist:
                    if la > 0:
                        f.write("\t\t,\n")
                    else:
                        f.write("\n")
                    f.write("\t\t{\n")
                    f.write('\t\t"Code":"%s"\n' % a[1])
                    f.write('\t\t,"Name":"%s"\n' % a[2])
                    f.write("\t\t}\n")
                    la += 1
                f.write("\t]\n")
                f.write("\t}\n")
                lc += 1
            f.write("]\n")
            f.write("}\n")
            lp += 1
        f.write("]\n")


if __name__ == '__main__':
    Write_json('write_json.txt', data)