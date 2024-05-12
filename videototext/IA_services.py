import whisper
import ollama

def transcripcion(url_file):
    model = whisper.load_model("base")
    result = model.transcribe(url_file)
    return result['text']


def resumen(texto):
    
    promt = f' De que trata el siguiente texto: {texto}, resume tu respuesta '
                                                                            
    resp = ollama.chat(model='phi3', messages =[
        
        {
            "role": "user",
            "content": promt,
        }
        
    ])

    return resp['message']['content']