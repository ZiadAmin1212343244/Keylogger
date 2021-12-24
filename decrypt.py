from cryptography.fernet import Fernet

key = input('Enter the key:')
fernet = Fernet(key.encode())

encMessage = input('Please enter the encrypted message')
encMessage = encMessage.encode()
decMessage = fernet.decrypt(encMessage).decode()
 
print("decrypted string: ", decMessage)


