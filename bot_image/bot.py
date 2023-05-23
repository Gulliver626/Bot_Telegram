import telebot # libreria para interactuar en telegram - pip install pyTelegramBotAPI
# activar uso de scripts Set-ExecutionPolicy RemoteSigned -Scope CurrentUser ​
token = '6161350290:AAHj7gRPh8tU7Cbei3Yclk0Nin9t6YHSAA4'
bot = telebot.TeleBot(token)

interacciones_alias = ['Ayuda', 'Comandos', 'Interacciones']

# --------------------- Contesta mensajes ---------------------
@bot.message_handler(content_types=['text', 'photo'])
def audio(message):
    #prueba audio
    if message.text == 'Audio':
        audio = open('audio.mp3', 'rb')
        bot.send_audio(message.chat.id, audio)
    #manda imagen
    elif message.text == 'Imagen':
        imagen = open('imagen.jpg', 'rb')
        bot.send_photo(message.chat.id, imagen)
    #interaccion con foto
    elif message.content_type == 'photo':
        try:
            mostrar = recibir_imagenes(message)
        except:
             bot.send_message(message.chat.id, 'No se ha podido reconocer el texto de la imagen')
    #muestra las interaccioens
    elif message.text in interacciones_alias:
        mostrar = interacciones(message) 
    elif message.text.startswith('Traducir'):
        mostrar = traducir(message)
    elif message.text.startswith('Corrige') or message.text.startswith('Mejora'
          ) or message.text.startswith('Parafrasea') or message.text.startswith('Dame'
          ) or message.text.startswith('Verifica'):
        mostrar = chatGPT(message)
    elif message.text.startswith('hola') or message.text.startswith('Hola'
        ) or message.text.startswith('Que tal') or message.text.startswith('que tal'
        ) or message.text.startswith('buen dia'):
        mostrar = chatGPT(message)
    else:
        bot.send_message(message.chat.id, "En qué te puedo ayudar?")

# --------------------- Conesta sin comandos ---------------------
# @bot.message_handler()
# def mandar_saludo(message):
#     bot.reply_to(message, 'Hola, ¿en qué puedo ayudarte?')

# --------------------- Contesta con el comando "/" ---------------------
# @bot.message_handler(commands=['start', 'hola'])
# def mandar_saludo(message):
#     bot.reply_to(message, 'Hola, ¿en qué puedo ayudarte?')
# @bot.message_handler(content_types=['photo'])

# --------------------- Mensaje de ayuda [muestra las intearacciones] ---------------------
def interacciones(message):
    # abrir el archivo
    with open('comandos.txt', encoding='utf-8') as archivo:
        contenido = archivo.read()
        print(contenido)
        bot.send_message(message.chat.id, contenido)

# --------------------- Mensaje de imagen [interacciín con foto] ---------------------
def recibir_imagenes(message):
     
     import uuid # libreria para nombre aleatoreo
     import os   # libreria para archivo temporal

     # Guardar la imagen
     file_id = message.photo[-1].file_id
     file_info = bot.get_file(file_id)
     downloaded_file = bot.download_file(file_info.file_path)
     # src = 'imagen.png' pero con nombre agregado
     src = 'imagen_{}.png'.format(uuid.uuid4())
     with open(src, 'wb') as new_file: # descarga la imagen para su uso
         new_file.write(downloaded_file)

         import cv2 # libreria para interactuar con imagenes - pip install opencv-contrib-python
         import pytesseract # libreria para leer texto de imagen - pip install pytesseract

         pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'             
             
         image = cv2.imread(src) #lee la imagen
         text = pytesseract.image_to_string(image)
         
         
     # Eliminar la imagen después de un tiempo determinado
     os.remove(src) 
      # Enviar mensaje al usuario
     
     bot.send_message(message.chat.id, text)

     from googletrans import Translator # pip install googletrans-py
     traductor = Translator()
        # Detectar el idioma del texto 
     idioma = traductor.detect(text).lang
        # Si el idioma es español, traducir al inglés
     if idioma == 'es':
        resultado = text
        # Si el idioma es distinto al español, traducir al español
     else:
        traduccion = traductor.translate(text, dest='es')
        resultado = traduccion.text
        bot.send_message(message.chat.id, resultado)         
        #Enviar la traducción 
    

     

     import openai # pip install openai
        
     openai.api_key = "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"
     cadena_unida = "corrige el siguiente texto: " + " " + resultado
     correct = openai.Completion.create(engine="text-davinci-003",
                                          prompt= cadena_unida,
                                          max_tokens=3000)
     corregido = correct.choices[0].text

     cadena_unida = "Dime los errores que tenga este texto: " + " " + resultado
     errrs = openai.Completion.create(engine="text-davinci-003",
                                          prompt= cadena_unida,
                                          max_tokens=3000)
     errores = errrs.choices[0].text

     cadena_unida2 = "mejora la redaccion del sig texto: " + " " + corregido
     redact = openai.Completion.create(engine="text-davinci-003",
                                          prompt= cadena_unida2,
                                          max_tokens=3000)
     redaccion = redact.choices[0].text

     cadena_unida2 = "parafrasea" + " " + corregido
     parafr = openai.Completion.create(engine="text-davinci-003",
                                          prompt= cadena_unida2,
                                          max_tokens=3000)
     parafrasear = parafr.choices[0].text
     
     from googletrans import Translator # pip install googletrans-py

     traductor = Translator()

     # Detectar el idioma del texto 
     idioma = traductor.detect(corregido).lang
     idioma = traductor.detect(redaccion).lang
     idioma = traductor.detect(parafrasear).lang
     # Si el idioma es español, traducir al inglés
     if idioma == 'es':
        trad = traductor.translate(corregido, dest='en')
        trad0 = traductor.translate(redaccion, dest='en') 
        trad1 = traductor.translate(parafrasear, dest='en')
     # Si el idioma es distinto al español, traducir al español
     else:
        trad = traductor.translate(corregido, dest='es')
        trad0 = traductor.translate(redaccion, dest='es')
        trad1 = traductor.translate(parafrasear, dest='es')
     #Enviar la traducción
     bot.send_message(message.chat.id, "Corregido") 
     bot.send_message(message.chat.id, corregido)

     bot.send_message(message.chat.id, "Errores") 
     bot.send_message(message.chat.id, errores)
     
     bot.send_message(message.chat.id, "Traducción") 
     bot.send_message(message.chat.id, trad.text)
    
     bot.send_message(message.chat.id, "Redacción") 
     bot.send_message(message.chat.id, redaccion)

     bot.send_message(message.chat.id, "Traducción")
     bot.send_message(message.chat.id, trad0.text)

     bot.send_message(message.chat.id, "Parafraseado") 
     bot.send_message(message.chat.id, parafrasear) 

     bot.send_message(message.chat.id, "Traducción")
     bot.send_message(message.chat.id, trad1.text)
      
def traducir(message):
    #Obtener el texto a traducir
        texto_a_traducir = message.text.split('Traducir ', 1)[1]
        print(texto_a_traducir)
        #Aquí iría el código para traducir
        traduccion = 'Aquí va la traducción:'     
        # import googletrans
        from googletrans import Translator # pip install googletrans-py

        traductor = Translator()

        # Detectar el idioma del texto 
        idioma = traductor.detect(texto_a_traducir).lang
        # Si el idioma es español, traducir al inglés
        if idioma == 'es':
            resultado = traductor.translate(texto_a_traducir, dest='en')
        # Si el idioma es distinto al español, traducir al español
        else:
            resultado = traductor.translate(texto_a_traducir, dest='es')
        
        #Enviar la traducción
        bot.reply_to(message, traduccion)
        bot.send_message(message.chat.id, resultado.text)

        


def chatGPT(message):
    import openai # pip install openai
        
    openai.api_key = "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"
        
    texto = message.text
 
    completion = openai.Completion.create(engine="text-davinci-003",
                                          prompt=texto,
                                          max_tokens=3000)
    print(completion.choices[0].text)
    bot.send_message(message.chat.id, completion.choices[0].text)
    
     
# --------------------------------------------------------
bot.polling()
while True: # Mantiene activo el bot
    pass
