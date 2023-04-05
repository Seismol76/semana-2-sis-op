import threading
import time
import random
import queue


BARBEROS =1
CLIENTES= 50
ASIENTOS = 4
ESPERAS = 1

def espera():
    time.sleep(ESPERAS * random.random())

class Barbero(threading.Thread):
    condicion = threading.Condition()
    alto_completado = threading.Event()

    def __init__(self, ID):
        super().__init__()
        self.ID = ID 
    
    def run(self):
        while True:
            try:
                cliente_actual =  sala_espera.get(block=False)
            except queue.Empty:
                if self.alto_completado.is_set():
                    return

                print(f"El barbero {self.ID} está durmiendo ahora... ")
                with self.condicion:
                    self.condicion.wait()
                    
            else:
                cliente_actual.cortar(self.ID)

class Cliente(threading.Thread):
    DURACION_CORTE = 3

    def __init__(self,ID):
        super().__init__()
        self.ID=ID

    def corte(self):
        time.sleep(self.DURACION_CORTE * random.random())

    def cortar(self, id_barbero):
        print(f"El barbero {id_barbero} está cortando el cabello del cliente {self.ID}")
        self.corte()
        print(f"El barbero {id_barbero} termino de cortar el cabello al cliente {self.ID}")
        self.atendido.set() 


    def run(self):
        self.atendido = threading.Event()

        try:
            sala_espera.put(self, block=False)
        except queue.Full: 
            print(f"No hay espacio en la sala de espera, {self.ID} se fue...")
            return

        print(f"El cliente {self.ID} se ha sentado en la sala de espera.")
        with Barbero.condicion:
            Barbero.condicion.notify(1)

        self.atendido.wait()    

if __name__ == "__main__":
    TODOS_CLIENTES = []
    sala_espera = queue.Queue(ASIENTOS)

    for i in range(BARBEROS):
        hilo_barbero = Barbero(i)
        hilo_barbero.start()

    for i in range(CLIENTES):
        espera()
        cliente = Cliente(i)
        TODOS_CLIENTES.append(cliente)
        cliente.start()
    
    for cliente in TODOS_CLIENTES:
        cliente.join()

    time.sleep(0.1)
    Barbero.alto_completado.set()
    with Barbero.condicion:
        Barbero.condicion.notify_all()

    print("La barberia ha cerrado.")
    
    