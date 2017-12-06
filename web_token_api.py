import endpoints
from google.appengine.ext import ndb
from google.appengine.api import app_identity
from protorpc import remote

import jwt
import time

from CustomExceptions import NotFoundException

from messages import EmailPasswordMessage, TokenMessage, CodeMessage, Token, TokenKey,MessageNone
from messages import EmpresaInput, EmpresaUpdate, EmpresaList
from messages import TweetInput, TweetUpdate, TweetList
from messages import UserInput, UserUpdate, UserList
from messages import DrumInput, DrumUpdate, DrumList
from messages import KeyboardInput, KeyboardUpdate, KeyboardList
from messages import BassInput, BassUpdate, BassList


from endpoints_proto_datastore.ndb import EndpointsModel

import models
from models import validarEmail
from models import Empresa, Usuarios, Tweet, Drum, Keyboard, Bass



###############
# Usuarios
###############
@endpoints.api(name='usuarios_api', version='v1', description='usuarios endpoints')
class UsuariosApi(remote.Service):
###############get the info of one########
 @endpoints.method(TokenKey, UserList, path='users/get', http_method='POST', name='users.get')
 def users_get(cls, request):
  try:                 
   token = jwt.decode(request.tokenint, 'secret')  #checa token
   userentity = ndb.Key(urlsafe=request.entityKey)
   user = Usuarios.get_by_id(userentity.id()) #obtiene usuario
            #user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = []  #crea lista
   lstMessage = UserList(code=1) # crea objeto mensaje
   lista.append(UserUpdate(token='', 
    entityKey= user.entityKey,
    #empresa_key = user.empresa_key.urlsafe(),
    email = user.email))
   lstMessage.data = lista#ASIGNA a la salida la lista
   message = lstMessage
  except jwt.DecodeError:
   message = UserList(code=-1, data=[]) #token invalido
  except jwt.ExpiredSignatureError:
   message = UserList(code=-2, data=[]) #token expiro
  return message


########################## list###################
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, UserList, path='users/list', http_method='POST', name='users.list')
 def lista_usuarios(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')  #checa token
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = []  #crea lista
   lstMessage = UserList(code=1) # crea objeto mensaje
   lstBd = Usuarios.query().fetch() # recupera de base de datos
   for i in lstBd: # recorre
    lista.append(UserUpdate(token='',
     entityKey=i.entityKey,
     #empresa_key=user.empresa_key.urlsafe(),
     email=i.email)) # agrega a la lista
    
   lstMessage.data = lista # la manda al messa
   message = lstMessage #regresa
    
  except jwt.DecodeError:
   message = UserList(code=-1, data=[]) #token invalido
  except jwt.ExpiredSignatureError:
   message = UserList(code=-2, data=[]) #token expiro
  return message

# delete
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, CodeMessage, path='users/delete', http_method='POST', name='users.delete')
 #siempre lleva cls y request
 def user_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   usersentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   usersentity.delete()#BORRA
   message = CodeMessage(code=1, message='Succesfully deleted')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# insert
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(UserInput, CodeMessage, path='users/insert', http_method='POST', name='users.insert')
 def user_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])
   if validarEmail(request.email) == False: #checa si el email esta registrado
                       #empresakey = ndb.Key(urlsafe=request.empresa_key) #convierte el string dado a entityKey
    if user.usuario_m(request, user.empresa_key)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
     codigo=1
    else:
     codigo=-3
                       #la funcion josue_m puede actualizar e insertar
                       #depende de la ENTRADA de este endpoint method
    message = CodeMessage(code=codigo, message='Succesfully added')
   else:
    message = CodeMessage(code=-4, message='El email ya ha sido registrado')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message


##login##

 @endpoints.method(EmailPasswordMessage, TokenMessage, path='users/login', http_method='POST', name='users.login')
 def users_login(cls, request):
  try:
   user = Usuarios.query(Usuarios.email == request.email).fetch() #obtiene el usuario dado el email
   if not user or len(user) == 0: #si no encuentra user saca
    raise NotFoundException()
   user = user[0] 
   keye = user.empresa_key.urlsafe() # regresa como mensaje el empresa key
   if not user.verify_password(request.password): # checa la contrasena
    raise NotFoundException()

   token = jwt.encode({'user_id': user.key.id(), 'exp': time.time() + 43200}, 'secret') #crea el token
   message = TokenMessage(token=token, message=keye, code=1) # regresa token
  except NotFoundException:
   message = TokenMessage(token=None, message='Wrong username or password', code=-1)
  return message

##update##
# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(UserUpdate, CodeMessage, path='user/update', http_method='POST', name='user.update')
#siempre lleva cls y request
 def user_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
   empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
   if user.usuario_m(request, empresakey)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='Sus cambios han sido guardados exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message


'''
'''

###########################
#### Empresa
###########################


## Google Cloud Endpoint
@endpoints.api(name='empresas_api', version='v1', description='empresas REST API')
class EmpresasApi(remote.Service):


# get one

 @endpoints.method(TokenKey, EmpresaList, path='empresa/get', http_method='POST', name='empresa.get')
#siempre lleva cls y request
 def empresa_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      #Obtiene el elemento dado el entityKey
   empresaentity = ndb.Key(urlsafe=request.entityKey)
      #CREA LA SALIDA de tipo JosueInput y le asigna los valores, es a como se declaro en el messages.py
      #empresaentity.get().empresa_key.urlsafe() para poder optener el EntityKey
     ##### ejemplo real
    ####### message = EmpresaList(code=1, data=[EmpresaUpdate(token='Succesfully get', nombre_empresa=empresaentity.get().nombre_empresa, empresa_key=empresaentity.get().empresa_key.urlsafe(), entityKey=empresaentity.get().entityKey)])
   message = EmpresaList(code=1, data = [EmpresaUpdate(token='Succesfully get',
    entityKey = empresaentity.get().entityKey,
    codigo_empresa=empresaentity.get().codigo_empresa, 
    nombre_empresa = empresaentity.get().nombre_empresa)])

  except jwt.DecodeError:
   message = EmpresaList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = EmpresaList(code=-2, data=[])
  return message




 @endpoints.method(TokenKey, CodeMessage, path='empresa/delete', http_method='POST', name='empresa.delete')
#siempre lleva cls y request
 def empresa_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   empresaentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   empresaentity.delete()#BORRA
   message = CodeMessage(code=1, message='Succesfully deleted')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message


# insert
 @endpoints.method(EmpresaInput, CodeMessage, path='empresa/insert', http_method='POST', name='empresa.insert')
#siempre lleva cls y request
 def empresa_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario models.py 
   myempresa = Empresa()
   if myempresa.empresa_m(request)==0: 
    codigo=1
   else:
		codigo=-3
      	      #la funcion josue_m puede actualizar e insertar
	      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=codigo, message='Succesfully added')
      #else:
	    #  message = CodeMessage(code=-4, message='Succesfully added')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message



# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(EmpresaUpdate, CodeMessage, path='empresa/update', http_method='POST', name='empresa.update')
#siempre lleva cls y request
 def empresa_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN 
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
      #empresakey = ndb.Key(urlsafe=request.empresa_key)#convierte el string dado a entityKey
   myempresa = Empresa()
   if myempresa.empresa_m(request)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='Sus cambios han sido guardados exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message



# list
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, EmpresaList, path='empresa/list', http_method='POST', name='empresa.list')
#siempre lleva cls y request
 def empresa_list(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   #if user.importante==1 or user.importante==2:
   lista = [] #crea lista para guardar contenido de la BD
   lstMessage = EmpresaList(code=1) #CREA el mensaje de salida
   lstBdEmpresa = Empresa.query().fetch() #obtiene de la base de datos
   for i in lstBdEmpresa: #recorre la base de datos
             #inserta a la lista creada con los elementos que se necesiten de la base de datos
             #i.empresa_key.urlsafe() obtiene el entityKey
	     #lista.append(ClientesUpdate(token='', nombre=i.nombre, status=i.status, empresa_key=i.empresa_key.urlsafe(), entityKey=i.entityKey))
    lista.append(EmpresaUpdate(token='', 
     entityKey = i.entityKey,
     codigo_empresa=i.codigo_empresa, 
     nombre_empresa = i.nombre_empresa))
      
   lstMessage.data = lista #ASIGNA a la salida la lista
   message = lstMessage
      #else:
      #    message = EmpresaList(code=-3, data=[])
  except jwt.DecodeError:
   message = EmpresaList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = EmpresaList(code=-2, data=[])
  return message


###########################
#### Tweets
###########################

@endpoints.api(name='tweet_api', version='v1', description='tweet REST API')
class TweetApi(remote.Service):
# get one
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, TweetList, path='tweet/get', http_method='POST', name='tweet.get')
#siempre lleva cls y request
 def tweet_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      #Obtiene el elemento dado el entityKey
   tweetentity = ndb.Key(urlsafe=request.entityKey)
      #CREA LA SALIDA de tipo JosueInput y le asigna los valores, es a como se declaro en el messages.py
      #josuentity.get().empresa_key.urlsafe() para poder optener el EntityKey
   message = TweetList(code=1, data=[TweetUpdate(token='Succesfully get',
    entityKey=tweetentity.get().entityKey,
    #empresa_key=teamentity.get().empresa_key.urlsafe(), 
    marcagui=tweetentity.get().marcagui, 
    modelogui=tweetentity.get().modelogui,
    cuerdas=tweetentity.get().cuerdas,
    precio=tweetentity.get().precio, 
    urlImage=tweetentity.get().urlImage)])
  except jwt.DecodeError:
   message = TweetList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = TweetList(code=-2, data=[])
  return message


# delete
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, CodeMessage, path='tweet/delete', http_method='POST', name='tweet.delete')
#siempre lleva cls y request
 def tweet_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   tweetentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   tweetentity.delete()#BORRA
   message = CodeMessage(code=0, message='tweet deleted')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# list
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, TweetList, path='tweet/list', http_method='POST', name='tweet.list')
#siempre lleva cls y request
 def tweet_list(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = [] #crea lista para guardar contenido de la BD
   lstMessage = TweetList(code=1) #CREA el mensaje de salida
   lstBd = Tweet.query().fetch() #obtiene de la base de datos
   for i in lstBd: #recorre la base de datos
    #inserta a la lista creada con los elementos que se necesiten de la base de datos
    #i.empresa_key.urlsafe() obtiene el entityKey
	     
    lista.append(TweetUpdate(token='', 
     entityKey=i.entityKey, 
     #empresa_key=i.empresa_key.urlsafe(),
     marcagui=i.marcagui, 
     modelogui=i.modelogui,
      cuerdas=i.cuerdas, 
       precio=i.precio,  
     urlImage=i.urlImage))
   lstMessage.data = lista #ASIGNA a la salida la lista
   message = lstMessage
  except jwt.DecodeError:
   message = TweetList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = TweetList(code=-2, data=[])
  return message

# insert
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TweetInput, CodeMessage, path='tweet/insert', http_method='POST', name='tweet.insert')
#siempre lleva cls y request
 def tweet_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de
   mytweet = Tweet()
   if mytweet.tweet_m(request, user.empresa_key)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
          #la funcion josue_m puede actualizar e insertar
          #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=codigo, message='Guitar added')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TweetUpdate, CodeMessage, path='tweet/update', http_method='POST', name='tweet.update')
#siempre lleva cls y request
 def tweet_update(cls, request):
  try:
   token = jwtser.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
   empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
   mytweet = Tweet()
   if mytweet.tweet_m(request, empresakey)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='Guitar updated')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message




###########################
#### Tweets
###########################

@endpoints.api(name='drum_api', version='v1', description='drum REST API')
class DrumApi(remote.Service):
# get one
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, DrumList, path='drum/get', http_method='POST', name='drum.get')
#siempre lleva cls y request
 def drum_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      #Obtiene el elemento dado el entityKey
   drumentity = ndb.Key(urlsafe=request.entityKey)
      #CREA LA SALIDA de tipo JosueInput y le asigna los valores, es a como se declaro en el messages.py
      #josuentity.get().empresa_key.urlsafe() para poder optener el EntityKey
   message = DrumList(code=1, data=[DrumUpdate(token='Succesfully get',
    entityKey=drumentity.get().entityKey,
    #empresa_key=teamentity.get().empresa_key.urlsafe(), 
    marcagui=drumentity.get().marcadrum, 
    modelogui=drumentity.get().modelodrum,
    cuerdas=drumentity.get().tambores,
    precio=drumentity.get().precio, 
    urlImage=drumentity.get().urlImage)])
  except jwt.DecodeError:
   message = DrumList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = DrumList(code=-2, data=[])
  return message


# delete
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, CodeMessage, path='drum/delete', http_method='POST', name='drum.delete')
#siempre lleva cls y request
 def drum_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   drumentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   drumentity.delete()#BORRA
   message = CodeMessage(code=0, message='drum deleted')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# list
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, DrumList, path='drum/list', http_method='POST', name='drum.list')
#siempre lleva cls y request
 def drum_list(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = [] #crea lista para guardar contenido de la BD
   lstMessage = DrumList(code=1) #CREA el mensaje de salida
   lstBd = Drum.query().fetch() #obtiene de la base de datos
   for i in lstBd: #recorre la base de datos
    #inserta a la lista creada con los elementos que se necesiten de la base de datos
    #i.empresa_key.urlsafe() obtiene el entityKey
       
    lista.append(DrumUpdate(token='', 
     entityKey=i.entityKey, 
     #empresa_key=i.empresa_key.urlsafe(),
     marcadrum=i.marcadrum, 
     modelodrum=i.modelodrum,
     tambores=i.tambores, 
       precio=i.precio,  
     urlImage=i.urlImage))
   lstMessage.data = lista #ASIGNA a la salida la lista
   message = lstMessage
  except jwt.DecodeError:
   message = DrumList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = DrumList(code=-2, data=[])
  return message

# insert
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(DrumInput, CodeMessage, path='drum/insert', http_method='POST', name='drum.insert')
#siempre lleva cls y request
 def drum_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de
   mydrum = Drum()
   if mydrum.drum_m(request, user.empresa_key)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
          #la funcion josue_m puede actualizar e insertar
          #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=codigo, message='Drum added')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(DrumUpdate, CodeMessage, path='drum/update', http_method='POST', name='drum.update')
#siempre lleva cls y request
 def drum_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
   empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
   mydrum = Drum()
   if mydrum.drum_m(request, empresakey)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='Guitar updated')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

###########################
#### Tweets
###########################

@endpoints.api(name='keyboard_api', version='v1', description='keyboard REST API')
class KeyboardApi(remote.Service):
# get one
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, KeyboardList, path='keyboard/get', http_method='POST', name='keyboard.get')
#siempre lleva cls y request
 def keyboard_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      #Obtiene el elemento dado el entityKey
   keyboardentity = ndb.Key(urlsafe=request.entityKey)
      #CREA LA SALIDA de tipo JosueInput y le asigna los valores, es a como se declaro en el messages.py
      #josuentity.get().empresa_key.urlsafe() para poder optener el EntityKey
   message = KeyboardList(code=1, data=[KeyboardUpdate(token='Succesfully get',
    entityKey=keyboardentity.get().entityKey,
    #empresa_key=teamentity.get().empresa_key.urlsafe(), 
    marcakey=keyboardentity.get().marcakey, 
    modelokey=keyboardentity.get().modelokey,
    teclas=keyboardentity.get().teclas,
    precio=keyboardentity.get().precio, 
    urlImage=keyboardentity.get().urlImage)])
  except jwt.DecodeError:
   message = KeyboardList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = KeyboardList(code=-2, data=[])
  return message


# delete
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, CodeMessage, path='keyboard/delete', http_method='POST', name='keyboard.delete')
#siempre lleva cls y request
 def keyboard_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   keyboardentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   keyboardentity.delete()#BORRA
   message = CodeMessage(code=0, message='keyboard deleted')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# list
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, KeyboardList, path='keyboard/list', http_method='POST', name='keyboard.list')
#siempre lleva cls y request
 def keyboard_list(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = [] #crea lista para guardar contenido de la BD
   lstMessage = KeyboardList(code=1) #CREA el mensaje de salida
   lstBd = Keyboard.query().fetch() #obtiene de la base de datos
   for i in lstBd: #recorre la base de datos
    #inserta a la lista creada con los elementos que se necesiten de la base de datos
    #i.empresa_key.urlsafe() obtiene el entityKey
       
    lista.append(KeyboardUpdate(token='', 
     entityKey=i.entityKey, 
     #empresa_key=i.empresa_key.urlsafe(),
     marcakey=i.marcakey, 
     modelokey=i.modelokey,
     tambores=i.tambores, 
       precio=i.precio,  
     urlImage=i.urlImage))
   lstMessage.data = lista #ASIGNA a la salida la lista
   message = lstMessage
  except jwt.DecodeError:
   message = KeyboardList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = KeyboardList(code=-2, data=[])
  return message

# insert
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(KeyboardInput, CodeMessage, path='keyboard/insert', http_method='POST', name='keyboard.insert')
#siempre lleva cls y request
 def keyboard_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de
   mykeyboard = Keyboard()
   if mykeyboard.keyboard_m(request, user.empresa_key)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
          #la funcion josue_m puede actualizar e insertar
          #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=codigo, message='Keyboard added')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(KeyboardUpdate, CodeMessage, path='keyboard/update', http_method='POST', name='keyboard.update')
#siempre lleva cls y request
 def keyboard_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
   empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
   mykeyboard = Keyboard()
   if mykeyboard.keyboard_m(request, empresakey)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='Guitar updated')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

###########################
#### Tweets
###########################

@endpoints.api(name='bass_api', version='v1', description='bass REST API')
class BassApi(remote.Service):
# get one
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, BassList, path='bass/get', http_method='POST', name='bass.get')
#siempre lleva cls y request
 def bass_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      #Obtiene el elemento dado el entityKey
   bassentity = ndb.Key(urlsafe=request.entityKey)
      #CREA LA SALIDA de tipo JosueInput y le asigna los valores, es a como se declaro en el messages.py
      #josuentity.get().empresa_key.urlsafe() para poder optener el EntityKey
   message = BassList(code=1, data=[BassUpdate(token='Succesfully get',
    entityKey=bassentity.get().entityKey,
    #empresa_key=teamentity.get().empresa_key.urlsafe(), 
    marcabass=bassentity.get().marcabass, 
    modelobass=bassentity.get().modelobass,
    cuerdas=bassentity.get().cuerdas,
    precio=bassentity.get().precio, 
    urlImage=bassentity.get().urlImage)])
  except jwt.DecodeError:
   message = BassList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = BassList(code=-2, data=[])
  return message


# delete
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, CodeMessage, path='bass/delete', http_method='POST', name='bass.delete')
#siempre lleva cls y request
 def bass_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   bassentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   bassentity.delete()#BORRA
   message = CodeMessage(code=0, message='bass deleted')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# list
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, BassList, path='bass/list', http_method='POST', name='bass.list')
#siempre lleva cls y request
 def bass_list(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = [] #crea lista para guardar contenido de la BD
   lstMessage = BassList(code=1) #CREA el mensaje de salida
   lstBd = Bass.query().fetch() #obtiene de la base de datos
   for i in lstBd: #recorre la base de datos
    #inserta a la lista creada con los elementos que se necesiten de la base de datos
    #i.empresa_key.urlsafe() obtiene el entityKey
       
    lista.append(BassUpdate(token='', 
     entityKey=i.entityKey, 
     #empresa_key=i.empresa_key.urlsafe(),
     marcabass=i.marcabass, 
     modelobass=i.modelobass,
     tambores=i.tambores, 
       precio=i.precio,  
     urlImage=i.urlImage))
   lstMessage.data = lista #ASIGNA a la salida la lista
   message = lstMessage
  except jwt.DecodeError:
   message = BassList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = BassList(code=-2, data=[])
  return message

# insert
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(BassInput, CodeMessage, path='bass/insert', http_method='POST', name='bass.insert')
#siempre lleva cls y request
 def bass_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de
   mybass = Bass()
   if mybass.bass_m(request, user.empresa_key)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
          #la funcion josue_m puede actualizar e insertar
          #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=codigo, message='Bass added')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(BassUpdate, CodeMessage, path='bass/update', http_method='POST', name='bass.update')
#siempre lleva cls y request
 def bass_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
   empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
   mybass = Bass()
   if mybass.bass_m(request, empresakey)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='Guitar updated')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message





application = endpoints.api_server([UsuariosApi, EmpresasApi, TweetApi,DrumApi,KeyboardApi,BassApi], restricted=False)

