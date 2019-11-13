import tkinter as tk
from tkinter import *
import json
import RPi.GPIO as GPIO
import requests


class Janela:
    def __init__(self, master, jsonpeixes):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        self.GPIO_MOTOR = 12 # Motor
        self.GPIO_LUZ = 32 # Luz

        GPIO.setup(self.GPIO_MOTOR, GPIO.OUT)
        GPIO.setup(self.GPIO_LUZ, GPIO.OUT)


        self.MOTOR = GPIO.PWM(self.GPIO_MOTOR, 200)
        self.LUZ = GPIO.PWM(self.GPIO_LUZ, 200)
        
        self.MOTOR.start(0)
        self.LUZ.start(0)
        
        self.master = master
        self.jsonpeixes = jsonpeixes

        self.master.attributes('-fullscreen',True) # DESCOMENTAR NO RASP

        cor = '#34ebde'

        self.master.title("")
        self.master.resizable(width=FALSE, height=FALSE)

        w_width, w_height = 800, 480
        self.master.minsize(w_width,w_height)
        
#Main frame
        self.main_frame = Frame(self.master ,width = w_width, height = w_height, bg = cor)
        self.main_frame.grid(sticky = 'nsew')

# Texto Raspeixe
        self.texto = Label(self.main_frame, text='Raspeixe!', bg = cor)
        self.texto['font']=('Verdana','40','bold')
        self.texto.grid(row = 0, column = 1, sticky = 'nsew')

# Drop down menu Nomes
        self.NomeVar = StringVar(self.master)
        self.NomeVar.set('Peixes')
        lista_nomes = list(self.jsonpeixes.keys())
        self.NomeMenu = OptionMenu(self.main_frame, self.NomeVar, *lista_nomes)
        self.NomeMenu.grid(column = 0 , row = 1)
        
# Drop down menu Nomes
        self.ComidaVar = StringVar(self.master)
        self.ComidaVar.set('Comidas')
        lista_comidas = list(self.jsonpeixes['Beta'].keys())
        self.ComidasMenu = OptionMenu(self.main_frame, self.ComidaVar, *lista_comidas)
        self.ComidasMenu.grid(column = 1 , row = 1)

# Buttons 
        self.BLigar = Button(self.main_frame , command = self.FuncLigar, text = 'Ligar')
        self.BLigar.grid( column = 2 , row = 1)

# Buttons 
        self.BCancelar = Button(self.main_frame , command = self.FuncCancelar, text = 'Cancelar')
        self.BCancelar.grid( column = 2 , row = 2, sticky = 'n')

# Set columns and rows
        col_count, row_count = self.main_frame.grid_size()
        for col in range(col_count):
            self.main_frame.grid_columnconfigure(col, minsize = w_width / 3)
        for row in range(row_count):
            self.main_frame.grid_rowconfigure(row, minsize = w_height / 3)
        self.ligado = False
        # Define rows and columns
        
        
    def GET(self):
        url = "http://industrial.api.ubidots.com/api/v1.6/devices/raspeixe/Bool/values/"
        headers = {
            'X-Auth-Token': "BBFF-hJMn4HQWBcYTH2408fyrUuly6aeRua",
            'Content-Type': "application/json",
            }
        
        response = requests.request("GET",url, headers=headers)
        return response.json()["results"][0]["value"]


    def NomeFunc(self, value):
        pass

    def ComidaFunc(self, value):
        pass

    def FuncLigar(self):
        
        ubidots_status = self.GET()
        
        if ubidots_status == 1.0:
        
            if (self.NomeVar.get() != 'Peixes')&(self.ComidaVar.get() != 'Comidas'):

                self.texto.config(fg = 'green')
                
                t_luz_on = self.jsonpeixes[self.NomeVar.get()][self.ComidaVar.get()]['Iluminacao_on']
                t_luz_off = self.jsonpeixes[self.NomeVar.get()][self.ComidaVar.get()]['Iluminacao_off']
                luz_hz = 1/(t_luz_on + t_luz_off)
                luz_dutyc = t_luz_on/(t_luz_off + t_luz_on)

                t_motor_on = self.jsonpeixes[self.NomeVar.get()][self.ComidaVar.get()]['Motor_on']
                t_motor_off = self.jsonpeixes[self.NomeVar.get()][self.ComidaVar.get()]['Motor_off']
                motor_hz = 1/(t_motor_on + t_motor_off)
                motor_dutyc = t_motor_on/(t_motor_on + t_motor_off)

                self.LUZ.ChangeFrequency(luz_hz)
                self.MOTOR.ChangeFrequency(motor_hz)

                self.LUZ.ChangeDutyCycle(luz_dutyc * 100)
                self.MOTOR.ChangeDutyCycle(motor_dutyc * 100)

                print('t on:',t_luz_on)
                print('t off:',t_luz_off)
                print('duty:',luz_dutyc)

    def FuncCancelar(self):
        self.texto.config(fg = 'red')
        self.MOTOR.ChangeDutyCycle(0)
        self.LUZ.ChangeDutyCycle(0)

with open('peixes.json') as json_file:
    jsonpeixes = json.load(json_file)
    
GPIO.cleanup()

raiz = Tk()
Janela(raiz, jsonpeixes)
raiz.mainloop()


#if __name__ == "__main__":
#    main()

