from django.shortcuts import render, redirect
from .forms import ArchivoForm


def response_form(request, form):
    return render(request, 'videototext/response_form.html', {'form': form})

def cargar_archivo(request):
    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES)
        print('hola')
        if form.is_valid():
            form.save()
            #return redirect('response_form/', form=form)
            #import whisper

            #def audio_a_texto(ruta):
             #   model = whisper.load_model("base")
            #    result = model.transcribe(ruta)

           # print(result["text"])
            print('hola',form)
            
    else:
        form = ArchivoForm()
    #return redirect('response_form/', form=form)