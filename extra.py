class Corriente(object):
    """
    Una clase para contener las propiedades necesarias para simular una corriente.
    """
    
    def __init__(self, Ti, Tf, WCp):
        self.Ti = float(Ti) #temperatura inicial
        self.Tf = float(Tf) #temperatura final
        self.Tpp= 0 #temperatura del punto de pliegue
        self.WCp = float(WCp)
        self.cal = Ti > Tf  #verdadero si la corriente es una corriente caliente
    
def enIntervalo(c, Ta, Tb):
    """
    Determina si la corriente c pasa por el intervalo de temperaturas [Ta, Tb].
    """
    
    if max([c.Ti, c.Tf]) > min([Ta, Tb]):
        if min([c.Ti, c.Tf]) < max([Ta, Tb]):
            return True
    else:
        return False
