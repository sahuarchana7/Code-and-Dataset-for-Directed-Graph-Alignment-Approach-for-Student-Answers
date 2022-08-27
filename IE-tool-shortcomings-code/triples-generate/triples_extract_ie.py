f2 = open('/location-where-to-store-output-files/outm_1.txt', 'w')

lookup = '1\t'
with open('/location-where-to-store-output-files/outm.txt') as f:
     f1 = f.readlines()
     for num, line in enumerate(f1):
        if lookup in line:
           
            ss = str(f1[num])
            ss1 = ss.split("\t")
            ss2 = "\t".join(ss1[1:])
            
            f2.write(ss2)
           

f.close()
f2.close()


f2 = open('/location-where-to-store-output-files/outs_1.txt', 'w')

lookup = '1\t'
with open('/location-where-to-store-output-files/outs.txt') as f:
     f1 = f.readlines()
     for num, line in enumerate(f1):
        if lookup in line:
            
            ss = str(f1[num])
            ss1 = ss.split("\t")
            ss2 = "\t".join(ss1[1:])
            
            f2.write(ss2)
           

f.close()
f2.close()




