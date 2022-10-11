from flask_bcrypt import Bcrypt
from getpass import getpass

bcrypt = Bcrypt()

### production password
passwd = getpass(prompt='Password:')

print("Here is your password for web. Copy only text inside in quotation marks!")
print(bcrypt.generate_password_hash(passwd))

### check password
#if bcrypt.check_password_hash(passwd, 'any password'):
#    print("Passwd success!")
