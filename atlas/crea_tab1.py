#1/usr/bin/env python
file_in = open('allCountries.txt','r')
file_out = open('all_gen.txt','w')
elenco=file_in.readlines()
file_in.close()
count = 1
for i in elenco:
    a=i.split('\t')
    stringa ="%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s"
    # print a[1], a[2], a[4], a[5], a[8], a[10], a[14], a[15], a[16]
    if int(a[14])>100:
        # for j in (1, 2, 4, 5, 8, 10, 14, 15, 17, 18):
        file_out.write(stringa % (a[1], a[2], a[4], a[5], a[8], a[10],
                                  a[11], a[12], a[13], a[14],
                                  a[16], a[17], a[18]))
file_out.close()
file_in.close()

##00 geonameid         : integer id of record in geonames database
##01 name              : name of geographical point (utf8) varchar(200)
##02 asciiname         : name of geographical point in plain ascii characters, varchar(200)
##03 alternatenames    : alternatenames, comma separated, ascii names automatically transliterated, convenience attribute from alternatename table, varchar(10000)
##04 latitude          : latitude in decimal degrees (wgs84)
##05 longitude         : longitude in decimal degrees (wgs84)
##06 feature class     : see http://www.geonames.org/export/codes.html, char(1)
##07 feature code      : see http://www.geonames.org/export/codes.html, varchar(10)
##08 country code      : ISO-3166 2-letter country code, 2 characters
##09 cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 60 characters
##10 admin1 code       : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)
##11 admin2 code       : code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80) 
##12 admin3 code       : code for third level administrative division, varchar(20)
##13 admin4 code       : code for fourth level administrative division, varchar(20)
##14 population        : bigint (8 byte int) 
##15 elevation         : in meters, integer
##16 dem               : digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat.
##17 timezone          : the timezone id (see file timeZone.txt) varchar(40)
##18 modification date : date of last modification in yyyy-MM-dd format
