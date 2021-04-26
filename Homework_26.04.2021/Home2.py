def tareri_qanak(mutqagrvatc_text,mutqagrvats_tar):
    count=0
    for tar in mutqagrvatc_text:
        if tar != mutqagrvats_tar:
            count+=1
        else:
            break
    return count
print(tareri_qanak("Hambal","b"))
