#!/usr/bin/python3
# -*- coding: latin-1 -*-

import sys
import numpy as np

def muestra_seno(t, frecuencia, amplitud=1.0, fase=0.0):
    return amplitud * np.sin(2 * np.pi * frecuencia * t + fase)

duracion_defecto = 1.0
duracion_minima  = 0.1
duracion_maxima  = 10.0

amplitud_defecto = 1.0
amplitud_minima  = 0.01
amplitud_maxima  = 1.0

muestras_por_segundo = 16000
fase = 0.0


if __name__ == '__main__':
    
    num_acciones = 0
    generar_wav = False
    generar_plot = False
    reproducir = False
    mostrar_ayuda = False
    
    duracion = duracion_defecto
    amplitud = amplitud_defecto
    
    i = 1
    
    while i < len(sys.argv):
        accion = sys.argv[i]
        
        if accion == 'wav':
            generar_wav = True
            num_acciones = num_acciones + 1
        elif accion == 'plot':
            generar_plot = True
            num_acciones = num_acciones + 1
        elif accion == 'play':
            reproducir = True
            num_acciones = num_acciones + 1
        
        elif accion == '--help' or accion == '-h':
            mostrar_ayuda = True
            num_acciones = num_acciones + 1
        
        elif accion == '--duracion' or accion == '-d':
            duracion = float(sys.argv[i+1])
            if duracion < duracion_minima or duracion > duracion_maxima:
                raise ValueError('Duracion invalida: %s (debe estar entre %s y %s)' % (sys.argv[i+1], duracion_minima, duracion_maxima))
            i = i + 1
        
        elif accion == '--amplitud' or accion == '-a':
            amplitud = float(sys.argv[i+1])
            if amplitud < amplitud_minima or amplitud > amplitud_maxima:
                raise ValueError('Amplitud invalida: %s (debe estar entre %s y %s)' % (sys.argv[i+1], amplitud_minima, amplitud_maxima))
            i = i + 1
        
        else:
            print('ERROR: Accion no reconocida: "%s"' % accion)
        i = i + 1
    
    if num_acciones == 0:
        print('ERROR: Ninguna accion especificada')
        print()
    
    if num_acciones == 0 or mostrar_ayuda:
        print('Uso:')
        print('    python %s [plot] [wav] [play] [OPTIONS]' % sys.argv[0])
        print()
        print('        --duracion DURACION, -d DURACION         especifica la duracion en segundos (%s - %s) (defecto=%s)' % (duracion_minima, duracion_maxima, duracion_defecto))
        print('        --amplitud AMPLITUD, -a AMPLITUD         especifica la amplitud (%s - %s) (defecto=%s)' % (amplitud_minima, amplitud_maxima, amplitud_defecto))
        print('        --help, -h                               muestra esta ayuda')
        print()

        sys.exit()

    notas = [
        ('do4',  261.63),
        ('re4',  293.66),
        ('mi4',  329.63),
        ('fa4',  349.23),
        ('sol4', 392.00),
        ('la4',  440.00),
        ('si4',  493.88),
        ('do5',  523.25),
    ]
    
    if generar_wav:
        import scipy.io.wavfile as wavfile
    
    if generar_plot:
        import matplotlib.pyplot as pyplot
        
    if reproducir:
        import sounddevice as sd
        sd.default.samplerate = muestras_por_segundo
    
    for nombre, frecuencia in notas:
        instantes = np.arange(muestras_por_segundo * duracion) / muestras_por_segundo
        muestras = np.array([muestra_seno(t, frecuencia, amplitud, fase) for t in instantes])
        
        if generar_wav:
            wavdata = np.array(muestras * 32766.0, dtype=np.int16)
            wavfile.write('out/nota_%s.wav' % nombre, muestras_por_segundo, wavdata)
        
        if generar_plot:
            pyplot.clf()
            pyplot.plot(instantes[0:100], muestras[0:100])
            pyplot.savefig('out/nota_%s.png' % nombre)
        
        if reproducir:
            sd.play(muestras, blocking=True)
            
