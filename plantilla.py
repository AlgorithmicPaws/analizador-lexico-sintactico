class AnalizadorSintactico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion = 0

        # Conjuntos de predicción para cada producción
        self.prediccion = {
            'S->ABC': {'seis', 'dos', 'cuatro'},
            'S->DE': {'uno', 'cuatro', 'tres'},
            'A->dosBtres': {'dos'},
            'A->ε': {'$', 'cinco', 'tres', 'cuatro'},
            'B\'->ε': {'cinco', '$', 'seis', 'tres'},
            'B\'->cuatroCcincoB\'': {'cuatro'},
            'B->ε': {'$', 'cinco', 'tres', 'seis'},
            'B->B\'': {'cuatro'},
            'C->seisAB': {'seis'},
            'C->ε': {'cinco', '$'},
            'D->unoAE': {'uno'},
            'D->B': {'cuatro'},
            'E->tres': {'tres'}
        }

    def match(self, tipo):
        if self.tokens[self.posicion][0] == tipo:
            self.posicion += 1
            return True
        else:
            print(f"<{self.tokens[self.posicion][2]}, {self.tokens[self.posicion][3]}> Error sintáctico: se encontró {self.tokens[self.posicion][0]}; se esperaba: {tipo}")
            quit()

    def analizar(self):
        # Llamar a la función de inicio del análisis sintáctico
        status = self.S()
        print(status)              #es True
        if status==None and (self.tokens[self.posicion][0] == '$'):
            print("El analisis sintactico ha finalizado exitosamente.")
            return True
        else:
            return False

    def S(self):
        if self.tokens[self.posicion][0] in self.prediccion['S->ABC']:
            self.A()
            self.B()
            self.C()
        elif self.tokens[self.posicion][0] in self.prediccion['S->DE']:
            self.D()
            self.E()
        else:
            print(f"<{self.tokens[self.posicion][2]}, {self.tokens[self.posicion][3]}> Error sintáctico: se encontró {self.tokens[self.posicion][0]} ; se esperaba: {self.prediccion['S->DE']}, {self.prediccion['S->ABC']}")
            quit()

    def A(self):
        if self.tokens[self.posicion][0] == 'dos':
            self.match('dos')
            self.B()
            self.match('tres')
        elif self.tokens[self.posicion][0] in self.prediccion['A->ε']:
            pass
        else:
            print("Error de sintaxis: No se pudo determinar la producción de A")
            return False

    def B(self):
        if self.tokens[self.posicion][0] in self.prediccion['B->B\'']:
            self.B_()
            
        elif self.tokens[self.posicion][0] in self.prediccion['B->ε']:
            pass
        else:
            print("Error de sintaxis: No se pudo determinar la producción de B")
            return False

    def B_(self):
        if self.tokens[self.posicion][0] == 'cuatro':
            self.match('cuatro')
            self.C()
            self.match('cinco')
            self.B_()
           
        elif self.tokens[self.posicion][0] in self.prediccion['B\'->ε']:
            pass
        else:
            print(f"<{self.tokens[self.posicion][2]}, {self.tokens[self.posicion][3]}> Error sintáctico: se encontró {self.tokens[self.posicion][0]} ; se esperaba: 'cuatro' ")
            quit()

    def C(self):
        if self.tokens[self.posicion][0] == 'seis':
            self.match('seis')
            self.A()
            self.B()
          
        elif self.tokens[self.posicion][0] in self.prediccion['C->ε']:
            pass
        else:
            print("Error de sintaxis: No se pudo determinar la producción de C")
            return False

    def D(self):
        if self.tokens[self.posicion][0] == 'uno':
            self.match('uno')
            self.A()
            self.E()
           
        elif self.tokens[self.posicion][0] in self.prediccion['D->B']:
            self.B()
        
        else:
            print("Error de sintaxis: No se pudo determinar la producción de D")
            return False

    def E(self):
        if self.tokens[self.posicion][0] == 'tres':
            self.match('tres')
       
        else:
            print("Error de sintaxis: No se pudo determinar la producción de E")
            return False


def main():
    # Ejemplo de lista de tokens para analizar
    tokens = [('cuatro', '4', 3, 2), 
              ('cinco', '5', 4, 4), 
              ('cuatro', '4', 6, 13), 
              ('cinco', '5', 6, 13),
              ('cuatro', '4', 6, 13), 
              ('cinco', '5', 6, 13), 
              ('siete', '7', 6, 13), 
              ('$', '$', 6, 13)]
    
    # Crear el analizador sintáctico y comenzar el análisis
    analizador = AnalizadorSintactico(tokens)
    analizador.analizar()

if __name__ == "__main__":
    main()

