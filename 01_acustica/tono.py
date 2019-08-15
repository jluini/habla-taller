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

mps_defecto = 16000
mps_minima = 1
mps_maxima = 100000000
fase = 0.0

if __name__ == '__main__':
    
    duracion = duracion_defecto
    amplitud = amplitud_defecto
    muestras_por_segundo = mps_defecto
    
    if len(sys.argv) < 2 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print('Uso:')
        print('    ptyhon %s FRECUENCIA [OPTIONS]' % sys.argv[0])
        print('        --duracion DURACION, -d DURACION         especifica la duracion en segundos (%s - %s) (defecto=%s)' % (duracion_minima, duracion_maxima, duracion_defecto))
        print('        --amplitud AMPLITUD, -a AMPLITUD         especifica la amplitud (%s - %s) (defecto=%s)' % (amplitud_minima, amplitud_maxima, amplitud_defecto))
        print('        --mps MUESTRAS_POR_SEGUNDO               numero de muestras por segundo (%s - %s) (defecto=%s)' % (mps_minima, mps_maxima, mps_defecto))
        print('        --help, -h                               muestra esta ayuda')
        print('')
        
        sys.exit()
    
    frecuencia = float(sys.argv[1])
    
    if frecuencia <= 0:
        raise ValueError('Frecuencia invalida: %s (debe ser un numero mayor a cero)' % sys.argv[1])
    
    i = 2
    
    while i < len(sys.argv):
        accion = sys.argv[i]
        
        if accion == '--duracion' or accion == '-d':
            if len(sys.argv) < i + 2:
                raise Exception('Se esperaba otro argumento despues de "%s"' % accion)
            duracion = float(sys.argv[i+1])
            if duracion < duracion_minima or duracion > duracion_maxima:
                raise ValueError('Duracion invalida: "%s" (debe estar entre %s y %s)' % (sys.argv[i+1], duracion_minima, duracion_maxima))
            i = i + 1
        
        elif accion == '--amplitud' or accion == '-a':
            if len(sys.argv) < i + 2:
                raise Exception('Se esperaba otro argumento despues de "%s"' % accion)
            amplitud = float(sys.argv[i+1])
            if amplitud < amplitud_minima or amplitud > amplitud_maxima:
                raise ValueError('Amplitud invalida: "%s" (debe estar entre %s y %s)' % (sys.argv[i+1], amplitud_minima, amplitud_maxima))
            i = i + 1
        
        elif accion == '--mps':
            if len(sys.argv) < i + 2:
                raise Exception('Se esperaba otro argumento despues de "%s"' % accion)
            muestras_por_segundo = float(sys.argv[i+1])
            if muestras_por_segundo < mps_minima or muestras_por_segundo > mps_maxima:
                raise ValueError('Numero invalido de muestras-por-segundo: "%s" (debe estar entre %s y %s)' % (sys.argv[i+1], mps_minima, mps_maxima))
            i = i + 1
        
        else:
            print('ERROR: Opcion no reconocida: "%s"' % accion)
        i = i + 1
    
    instantes = np.arange(muestras_por_segundo * duracion) / muestras_por_segundo
    muestras = np.array([muestra_seno(t, frecuencia, amplitud, fase) for t in instantes])

    import sounddevice as sd
    sd.default.samplerate = muestras_por_segundo
    sd.play(muestras, blocking=True)
    
