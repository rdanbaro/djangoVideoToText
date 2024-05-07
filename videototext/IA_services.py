import whisper

def transcripcion(url_file):
    model = whisper.load_model("base")
    result = model.transcribe(url_file)
    return result['text']