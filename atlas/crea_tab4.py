file_in = open("ISO 3166 Codes (Countries).csv")
                 
cnt = file_in.readlines()
lista = []
for i in cnt:
    lista.append(i.split(';'))
file_out = open('all_countries.txt', 'w')
for i in lista:
    file_out.write("{};{}\n".format(i[0].strip(),i[1].strip()))
file_out.close()
file_in.close()

