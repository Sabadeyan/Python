try:
    my_file = open("how-to-turn-dirt-into-gold.txt", "r")
    my_txt = my_file.read()
    my_txt = my_txt.lower()
    my_txt = my_txt.replace('"', ' " ')
    my_txt = my_txt.replace(',', ' , ')
    my_txt = my_txt.replace('.', ' . ')
    my_list = my_txt.split()
    qanak_if = my_list.count('if')
    qanak_the = my_list.count('the')
    qanak_e = my_txt.count('e')
    my_file.close()
except IOError:
    qanak_if=-1
    qanak_the=-1
    qanak_e=-1
finally:
    new_file=open('statistics.txt','w')
    new_file.write('qanak_if '+ str(qanak_if) + '\n')
    new_file.write('qanak_the '+ str(qanak_the) +'\n')
    new_file.write('qanak_e '+ str(qanak_e) +'\n')
    new_file.close()



