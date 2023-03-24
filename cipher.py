cipher = input("Enter the password to encrypt: ")
ency_value = int(input("enter the number for encryption: "))

text = ''

for char in cipher:
    if not char.isalpha():
        continue
    char = char.upper()
    code = ord(char) + ency_value
    text += chr(code)

print(text)
