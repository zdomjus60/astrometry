#1/usr/bin/env python
file_in = open('admin2Codes.txt','r')
file_out = open('all_admin2.txt','w')
elenco=file_in.readlines()
file_in.close()

for i in elenco:
    a=i.split('\t')
    b = a[0].split('.')
    stringa = "{};{};{};{};{};{}"
    file_out.write(stringa.format(b[0],b[1],b[2],a[1],a[2],a[3]))

file_out.close()
file_in.close()
