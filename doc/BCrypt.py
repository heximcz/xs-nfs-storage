from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

### production password
#print(bcrypt.generate_password_hash('any password'))

### Store password here
#passwd = '$2b$12$nedngTnzSX3vxOzwabsZUOcOOKnfm7GRKweN.QhyEwEJnU2b48Koe'

### check password
#if bcrypt.check_password_hash(passwd, 'any password'):
#    print("Passwd success!")
