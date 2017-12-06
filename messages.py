from protorpc import messages
from protorpc import message_types

class MessageNone(messages.Message):
    inti = messages.StringField(1)
# Input messages
#Recibe el token para validar
class Token(messages.Message):
    tokenint = messages.StringField(1, required=True)
    #entityKey = messages.StringField(2, required=False)
    #fromurl = messages.StringField(3)

#Recibe el token y un entityKey de cualquier base de datos para validar
class TokenKey(messages.Message):
    tokenint = messages.StringField(1, required=True)
    entityKey = messages.StringField(2, required=True)
    #fromurl = messages.StringField(3)


#Recibe el email y contrasena para la creacion de token
class EmailPasswordMessage(messages.Message):
    email = messages.StringField(1, required=True)
    password = messages.StringField(2, required=True)

# Output messages
#regresa un token
class TokenMessage(messages.Message):
    code = messages.IntegerField(1)
    message = messages.StringField(2)
    token = messages.StringField(3)

#regresa mensajes de lo ocurrido
class CodeMessage(messages.Message):
    code = messages.IntegerField(1)
    message = messages.StringField(2)

#USERS
class UserInput(messages.Message):
    token = messages.StringField(1) 
    empresa_key = messages.StringField(2)
    email = messages.StringField(3)
    password = messages.StringField(4)



class UserUpdate(messages.Message):
    token = messages.StringField(1)
    email = messages.StringField(2)
    password = messages.StringField(3)
    entityKey = messages.StringField(4, required=True)

class UserList(messages.Message):
    code = messages.IntegerField(1)
    data = messages.MessageField(UserUpdate, 2, repeated=True)


######Empresa########

#Mensaje de Entrada y Salida para la base de datos Empresa
class EmpresaInput(messages.Message):
    token = messages.StringField(1, required=True) 
    codigo_empresa = messages.StringField(2)
    nombre_empresa = messages.StringField(3)


class EmpresaUpdate(messages.Message):
    token = messages.StringField(1, required=True)
    entityKey = messages.StringField(2, required=True)
    codigo_empresa = messages.StringField(3)
    nombre_empresa = messages.StringField(4)



#regresa una lista para la base de datos Empresa
class EmpresaList(messages.Message):
    code = messages.IntegerField(1)
#regresa mensaje de lo ocurrido
#mensaje de tipo MENSAJEFIELD que regresa una lista de tipo EmpresaUpdate
#es necesario el repeated para que sea lista
    data = messages.MessageField(EmpresaUpdate, 2, repeated=True)


######Team########

#Mensaje de Entrada y Salida para Tweets
class TweetInput(messages.Message):
    token = messages.StringField(1, required=True) 
    marcagui = messages.StringField(2)
    modelogui = messages.StringField(3)
    cuerdas = messages.StringField(4)
    precio = messages.StringField(6)
    urlImage = messages.StringField(5)

    
class TweetUpdate(messages.Message):
    token = messages.StringField(1, required=True)
    #empresa_key = messages.StringField(2, required=True)
    entityKey = messages.StringField(2, required=True)
    marcagui = messages.StringField(3)
    modelogui = messages.StringField(4)
    cuerdas = messages.StringField(5)
    precio = messages.StringField(6)
    urlImage = messages.StringField(7)

#regresa una lista para la base de datos Empresa
class TweetList(messages.Message):
    code = messages.IntegerField(1)
#regresa mensaje de lo ocurrido
#mensaje de tipo MENSAJEFIELD que regresa una lista de tipo TeamUpdate
#es necesario el repeated para que sea lista
    data = messages.MessageField(TweetUpdate, 2, repeated=True)

class DrumInput(messages.Message):
    token = messages.StringField(1, required=True) 
    marcadrum = messages.StringField(2)
    modelodrum = messages.StringField(3)
    tambores = messages.StringField(4)
    precio = messages.StringField(6)
    urlImage = messages.StringField(5)

    
class DrumUpdate(messages.Message):
    token = messages.StringField(1, required=True)
    #empresa_key = messages.StringField(2, required=True)
    entityKey = messages.StringField(2, required=True)
    marcadrum = messages.StringField(3)
    modelodrum = messages.StringField(4)
    tambores = messages.StringField(5)
    precio = messages.StringField(6)
    urlImage = messages.StringField(7)

#regresa una lista para la base de datos Empresa
class DrumList(messages.Message):
    code = messages.IntegerField(1)
#regresa mensaje de lo ocurrido
#mensaje de tipo MENSAJEFIELD que regresa una lista de tipo TeamUpdate
#es necesario el repeated para que sea lista
    data = messages.MessageField(DrumUpdate, 2, repeated=True)

class KeyboardInput(messages.Message):
    token = messages.StringField(1, required=True) 
    marcakey = messages.StringField(2)
    modelokey = messages.StringField(3)
    teclas = messages.StringField(4)
    precio = messages.StringField(6)
    urlImage = messages.StringField(5)

    
class KeyboardUpdate(messages.Message):
    token = messages.StringField(1, required=True)
    #empresa_key = messages.StringField(2, required=True)
    entityKey = messages.StringField(2, required=True)
    marcakey = messages.StringField(3)
    modelokey = messages.StringField(4)
    teclas = messages.StringField(5)
    precio = messages.StringField(6)
    urlImage = messages.StringField(7)

#regresa una lista para la base de datos Empresa
class KeyboardList(messages.Message):
    code = messages.IntegerField(1)
#regresa mensaje de lo ocurrido
#mensaje de tipo MENSAJEFIELD que regresa una lista de tipo TeamUpdate
#es necesario el repeated para que sea lista
    data = messages.MessageField(KeyboardUpdate, 2, repeated=True)

class BassInput(messages.Message):
    token = messages.StringField(1, required=True) 
    marcabass = messages.StringField(2)
    modelobass = messages.StringField(3)
    cuerdas = messages.StringField(4)
    precio = messages.StringField(6)
    urlImage = messages.StringField(5)

    
class BassUpdate(messages.Message):
    token = messages.StringField(1, required=True)
    #empresa_key = messages.StringField(2, required=True)
    entityKey = messages.StringField(2, required=True)
    marcabass = messages.StringField(3)
    modelobass = messages.StringField(4)
    cuerdas = messages.StringField(5)
    precio = messages.StringField(6)
    urlImage = messages.StringField(7)

#regresa una lista para la base de datos Empresa
class BassList(messages.Message):
    code = messages.IntegerField(1)
#regresa mensaje de lo ocurrido
#mensaje de tipo MENSAJEFIELD que regresa una lista de tipo TeamUpdate
#es necesario el repeated para que sea lista
    data = messages.MessageField(KeyboardUpdate, 2, repeated=True)



    
