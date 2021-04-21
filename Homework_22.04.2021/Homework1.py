def is_palindrome(ourstring):
    for i in range(len(ourstring)//2+1):
        if ourstring [i]!=ourstring[-1-i]:
            return False
    return True
print(is_palindrome("12345665432"))


