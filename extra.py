class Corriente(object):
    """
    Una clase para crear objetos tipo Corriente.
    """
    
    def __init__(self, Ti, Tf, WCp):
        self.Ti = float(Ti) #temperatura inicial
        self.Tf = float(Tf) #temperatura final
        self.Tpp= 0 #temperatura del punto de pliegue
        self.WCp = float(WCp)
        self.cal = Ti > Tf  #Verdadero si la corriente es una corriente caliente
