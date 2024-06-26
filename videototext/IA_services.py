import whisper
import ollama

def transcripcion(url_file):
    model = whisper.load_model("base")
    result = model.transcribe(url_file)
    return result['text']


def resumen(texto):
    texto_prueba = '''
    Bienvenidos a mi caminotech. Hoy estaremos hablando sobre errores comunes que se cometen a la hora 
    de empezar a por amar en Python. Ahordaremos algunos consejos útiles para evitar estos errores
    y mejorar rápidamente en este bello lenguaje de programación. Así que sin más, comencemos. 
    Hola amigos, bienvenidos a mi caminotech. Hoy estaremos hablando sobre errores comunes que se cometen 
    a la hora de empezar a por amar en Python. Ahordaremos algunos consejos útiles para evitar estos errores 
    y mejorar rápidamente en este bello lenguaje de programación. Así que sin más, comencemos. 
    Pues vale, digamos que ya elegimos a Python. Es nuestro primer amor en cuanto a lenguaje de programación. 
    Ya tenemos creado y configurado nuestro entorno y ya vamos a empezar a programar. 
    Y aquí los consejos para evitar los errores y tener mejor experiencia de desarrollo con este lenguaje. 
    Número 1.
    '''
    contexto = '''
    Eres un experto haciendo resumenes, y vas a ayudarme a resumir videos de una plataforma estilo Youtube.
    Te voy a dar la trancripcion de un video y me vas a decir de que trata, no me des 
    la transcripcion completa, solo quiero el resumen en un solo parrafo. No me des varias opciones
    para escoger,  la respuesta solo la quiero en español. Ten en cuenta que todo esto es parte de una sola instruccion

    '''
    
    prompt = f' Teneniendo en cuenta que {contexto} la transcripcion del video es el siguiente: {texto}'
                                                                            
    resp = ollama.chat(model='phi3', messages =[
        
        {
            "role": "user",
            "content": prompt,
        }
        
    ])
    resp_temp = resp['message']['content'].split('.')
    resp_definitiva = '.'.join(resp_temp[0:-1])
    return resp_definitiva


def palabras_clave(texto):
    
    texto_prueba = ''' 
    Bienvenidos a mi caminotech. Hoy estaremos hablando sobre errores comunes que se cometen a la hora 
    de empezar a por amar en Python. Ahordaremos algunos consejos útiles para evitar estos errores
    y mejorar rápidamente en este bello lenguaje de programación. Así que sin más, comencemos. 
    Hola amigos, bienvenidos a mi caminotech. Hoy estaremos hablando sobre errores comunes que se cometen 
    a la hora de empezar a por amar en Python. Ahordaremos algunos consejos útiles para evitar estos errores 
    y mejorar rápidamente en este bello lenguaje de programación. Así que sin más, comencemos. 
    Pues vale, digamos que ya elegimos a Python. Es nuestro primer amor en cuanto a lenguaje de programación. 
    Ya tenemos creado y configurado nuestro entorno y ya vamos a empezar a programar. 
    Y aquí los consejos para evitar los errores y tener mejor experiencia de desarrollo con este lenguaje. 
    Número 1.
    '''
    
    
    
    
    contexto = '''"Actua como un experto extrayendo palabras claves de un texto,
    Sacame las palabras clave para etiquetar dicho texto, ten en cuenta que dicho texto, es
    la transcripcion de un video, por tanto las palabras claves seran las palabras con las 
    que se puedan resumir el contenido del video. , dame un minimo de 4 palbras claves. Solo quiero las palabras claves del video, 
    obvia cualquier otro texto, Devuelveme estas palabras en una lista
    dividada por comas.No pongas ningun enunciado, solo quiero las palabras. El el texto es el siguiente:" \n
    
    '''
    
    prompt = f'{contexto} {texto}'
    
    resp = ollama.chat(model='phi3', messages =[
        
        {
            "role": "user",
            "content": prompt,
        }
        
    ])
    #print (resp['message']['content'])
    resp_definitiva = resp['message']['content'].split(',')
    return resp_definitiva[:-1]