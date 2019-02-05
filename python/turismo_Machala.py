import couchdb  # Libreria de CouchDB (requiere ser instalada primero)
from tweepy import Stream  # tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json  # Libreria para manejar archivos JSON

###Credenciales de la cuenta de Twitter########################
# Poner aqui las credenciales de su cuenta privada, caso contrario la API bloqueara esta cuenta de ejemplo

#ckey = "unksC6a2wXM5JoZ5cFwqxD8F6"
#csecret = "EJiqOoTUSQIPNLQpTgJnDFk6IJsjpt7EzeD7sgBGOGl43HCWm0"
#atoken = "999027538243588098-gAoMQKa1Na0YSvHB3g5Q9558jXCMSgQ"
#asecret = "UcQU3N0SibSMRHbekjYjG1eBjuwaqPJpnKYMfspiQZ6jN"

#ckey = "lUoRijvESyV0YtnxgkyfNaGDy"
#csecret = "dIc3fcJ8qYcV7wfIDN58IxmmjTKzIWWONfffxLESFpF9nKFTYn"
#atoken = "115946548-Li5UYIG0FjqxeFodjKFfWVBhqIYn3c8kRBWAVx7I"
#asecret = "BnVWGORJjNQOlCMcu6al5O3QvR0yKmOGRsY3b7p41jIOp"

ckey = "b0hhIO0RfXbsgPjjBSlcAOEkB"
csecret = "3825kTPBIf0CkktKEZ1Q5aMjJe9HqMq8RD9P3sX0Tz1gf0p0dd"
atoken = "1268502774-9G1na0czUOXCbiac8hs3S31c976JHExouRJGm5c"
asecret = "PAhtCrPxacjS2AmTyIOCSKmGfPQzuF9jll07n2bT7ptgr"	

#ckey = "unksC6a2wXM5JoZ5cFwqxD8F6"
#csecret = "EJiqOoTUSQIPNLQpTgJnDFk6IJsjpt7EzeD7sgBGOGl43HCWm0"
#atoken = "999027538243588098-gAoMQKa1Na0YSvHB3g5Q9558jXCMSgQ"
#asecret = "UcQU3N0SibSMRHbekjYjG1eBjuwaqPJpnKYMfspiQZ6jN"

#####################################

class listener(StreamListener):
    def on_data(self, data):
        dictTweet = json.loads(data)
        try:
            dictTweet["_id"] = str(dictTweet['id'])
            # Antes de guardar el documento puedes realizar parseo, limpieza y cierto analisis o filtrado de datos previo
            # a guardar en documento en la base de datos
            doc = db.save(dictTweet)  # Aqui se guarda el tweet en la base de couchDB
            print("Guardado " + "=> " + dictTweet["_id"])
        except:
            print("Documento ya existe")
            pass
        return True

    def on_error(self, status):
        print(status)


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

# Setear la URL del servidor de couchDB
server = couchdb.Server('http://admin:1234@localhost:5984/')
try:
    # Si no existe la Base de datos la crea
    db = server.create('machala')
except:
    # Caso contrario solo conectarse a la base existente
    db = server['machala']

# Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
twitterStream.filter(track=["Machala","turismo"])
# twitterStream.filter(locations=[-78.586922,-0.395161,-78.274155,0.021973])
