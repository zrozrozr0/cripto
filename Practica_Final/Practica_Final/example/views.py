from django.shortcuts import render, redirect
from django.contrib import messages
from example.firma import signature, validate
from example.AES import C_S,D_V
def MainPage(request):
    return render(request, 'example/index.html')

def FimaDigitalPage(request):
    return render(request, 'example/Final.html')

def Todo(request, msgfile, pkfile,pubkfile):
    message = C_S(msgfile, pkfile,pubkfile)
    if(len(message) == 17):
        messages.add_message(request, messages.SUCCESS, message, extra_tags='Firma_txt')
    else:
        messages.add_message(request, messages.ERROR, message, extra_tags='Firma_txt')
    return redirect('ds')

def TodoInverso(request, msgfile,pubkfile, pkfile):
    message = D_V(msgfile, pkfile,pubkfile)
    if(len(message) == 34):
        messages.add_message(request, messages.SUCCESS, message, extra_tags='Validate_txt')
    else:
        messages.add_message(request, messages.ERROR, message, extra_tags='Validate_txt')
    return redirect('ds')

def Firmar(request, msgfile, pkfile):
    message = signature(msgfile, pkfile)
    if(len(message) == 24):
        messages.add_message(request, messages.SUCCESS, message, extra_tags='Firma_txt')
    else:
        messages.add_message(request, messages.ERROR, message, extra_tags='Firma_txt')
    return redirect('ds')
    
def Validar(request, msgfile, pkfile):
    message = validate(msgfile, pkfile)
    print(len(message))
    if(len(message) == 19):
        messages.add_message(request, messages.SUCCESS, message , extra_tags='Validate_txt')
    else:
        messages.add_message(request, messages.ERROR, message, extra_tags='Validate_txt')
    return redirect('ds')
