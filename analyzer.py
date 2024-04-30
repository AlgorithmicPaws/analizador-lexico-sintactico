class AnalizadorSintactico:
    def __init__(self, tokens, gramatica, simboloInicial):
        self.tokens = tokens
        self.posicion = 0

        """
        # Conjuntos de predicción para cada producción
        self.prediccion = {
            'E->ε': {'$', 'tk_right_parenthesis'},
            'E->+TE': {'tk_plus'},
            'E->-TE': {'tk_minus'},
            'S->TE': {'tk_left_parenthesis', 'Id'},
            'Z->ε': {'$', 'tk_right_parenthesis', 'tk_plus', 'tk_minus'},
            'Z->/FZ': {'tk_slash'},
            'Z->*FZ': {'tk_asterisk'},
            'T->FZ': {'tk_left_parenthesis', 'Id'},
            'F->ident': {'Id'},
            'F->(S)': {'tk_left_parenthesis'}
        }"""
        self.prediccion = sacarConjuntos(gramatica, simboloInicial)

    def match(self, tipo):
        if self.tokens[self.posicion][0] == tipo:
            self.posicion += 1
            return True
        else:
            self.error(tipo)

    def analizar(self):
        # Llamar a la función de inicio del análisis sintáctico
        status = self.S()
        if status==None and (self.tokens[self.posicion][0] == '$'):
            print("El análisis sintáctico ha finalizado exitosamente.")
            return True
        else:
            self.error(self.tokens[self.posicion][0])

    def error(self, expected):
        new_expected = []
        symbols = {
    'tk_plus': '+', 'tk_minus': '-', 'tk_asterisk': '*', 'tk_double_asterisk': '**',
    'tk_slash': '/', 'tk_double_slash': '//', 'tk_percent': '%', 'tk_at': '@',
    'tk_left_shift': '<<', 'tk_right_shift': '>>', 'tk_ampersand': '&', 'tk_pipe': '|',
    'tk_caret': '^', 'tk_tilde': '~', 'tk_walrus': ':=',
    'tk_less_than': '<', 'tk_greater_than': '>', 'tk_less_than_or_equal_to': '<=',
    'tk_greater_than_or_equal_to': '>=', 'tk_equal_to': '==', 'tk_not_equal_to': '!=',
    'tk_left_parenthesis': '(', 'tk_right_parenthesis': ')',
    'tk_left_square_bracket': '[', 'tk_right_square_bracket': ']',
    'tk_left_curly_brace': '{', 'tk_right_curly_brace': '}',
    'tk_comma': ',', 'tk_colon': ':', 'tk_dot': '.', 'tk_semicolon': ';', 'tk_equal': '=',
    'tk_arrow': '->', 'tk_plus_equal': '+=', 'tk_minus_equal': '-=',
    'tk_multiply_equal': '*=', 'tk_divide_equal': '/=', 'tk_double_divide_equal': '//=',
    'tk_modulus_equal': '%=', 'tk_at_equal': '@=', 'tk_and_equal': '&=', 'tk_or_equal': '|=',
    'tk_xor_equal': '^=', 'tk_right_shift_equal': '>>=', 'tk_left_shift_equal': '<<=',
    'tk_double_asterisk_equal': '**=', 'tk_exclamation': '!', 'tk_backslash': '\\'
}

        if type(expected) == str:
            if expected in symbols:
                print(f"<{self.tokens[self.posicion][-2]}, {self.tokens[self.posicion][-1]}> Error sintáctico: se encontró '{self.tokens[self.posicion][-3]}' ; se esperaba: {symbols[expected]}")
            else:
                print(f"<{self.tokens[self.posicion][-2]}, {self.tokens[self.posicion][-1]}> Error sintáctico: se encontró '{self.tokens[self.posicion][-3]}' ; se esperaba: {expected}")
        else:
            for prediction in expected:
                if type(prediction) == set:
                    for prediction_item in prediction:
                        if prediction_item in symbols:
                            new_expected.append(symbols[prediction_item])
                        else:
                            new_expected.append(prediction_item)
                else:
                    if prediction in symbols:
                        new_expected.append(symbols[prediction])
                    else:
                        new_expected.append(prediction)
            expected_string = ", ".join(new_expected)
            print(f"<{self.tokens[self.posicion][-2]}, {self.tokens[self.posicion][-1]}> Error sintáctico: se encontró '{self.tokens[self.posicion][-3]}' ; se esperaba: {expected_string}")

        quit()

    def S(self):
        expected = [self.prediccion['S->TE']]
        if self.tokens[self.posicion][0] in expected[0]:
            self.T()
            self.E()
        else:
            self.error(expected)

    def E(self):
        expected = [self.prediccion['E->ε'], self.prediccion['E->tk_plusTE'], self.prediccion['E->tk_minusTE']]
        if self.tokens[self.posicion][0] in expected[0]:
            pass
        elif self.tokens[self.posicion][0] in expected[1]:
            self.match('tk_plus')
            self.T()
            self.E()
        elif self.tokens[self.posicion][0] in expected[2]:
            self.match('tk_minus')
            self.T()
            self.E()
        else:
            self.error(expected)

    def Z(self):
        expected = [self.prediccion['Z->ε'], self.prediccion['Z->tk_slashFZ'], self.prediccion['Z->tk_asteriskFZ']]
        if self.tokens[self.posicion][0] in expected[0]:
            pass
        elif self.tokens[self.posicion][0] in expected[1]:
            self.match('tk_slash')
            self.F()
            self.Z()
        elif self.tokens[self.posicion][0] in expected[2]:
            self.match('tk_asterisk')
            self.F()
            self.Z()
        else:
            self.error(expected)

    def T(self):
        expected = [self.prediccion['T->FZ']]
        if self.tokens[self.posicion][0] in expected[0]:
            self.F()
            self.Z()
        else:
            self.error(expected)

    def F(self):
        expected = [self.prediccion['F->Id'], self.prediccion['F->tk_left_parenthesisStk_right_parenthesis']]
        if self.tokens[self.posicion][0] in expected[0]:
            self.match('Id')
        elif self.tokens[self.posicion][0] in expected[1]:
            self.match('tk_left_parenthesis')
            self.S()
            self.match('tk_right_parenthesis')
        else:
            self.error(expected)

#Recap Primer Taller
def sacarConjuntos(gramatica, simboloInicial):

    def calcular_primeros(gramatica):
        primeros = {}
        
        # Función auxiliar para determinar si un símbolo es terminal
        def es_terminal(simbolo):
            return simbolo not in gramatica.keys()

        # Función recursiva para calcular los primeros de un símbolo
        # PRIMEROS(αlpha) = primeros
        # PRIMEROS(a1) = primeros_del_simbolo
        def calcular_primeros_rec(simbolo):
            # Si ya hemos calculado los primeros para este símbolo, regresar
            if simbolo in primeros:
                return primeros[simbolo]
            
            primeros[simbolo] = set()
            
            # Regla 1: Si es épsilon, agregar épsilon
            if simbolo == 'ε':
                primeros[simbolo].add('ε')
                return primeros[simbolo]
            
            #symbol itera todos los no term. y simbolo es la regla actual
            for produccion in gramatica[simbolo]:
                # Regla 2a: Si es un terminal, agregarlo
                if es_terminal(produccion[0]):
                    primeros[simbolo].add(produccion[0])
                # Regla 2b, 2c, 2d: Si es un no terminal, calcular primeros recursivamente
                else:
                    for i, symbol in enumerate(produccion):
                        if es_terminal(symbol):
                            primeros[simbolo].add(symbol)
                            break
                        #regla 2d: se llama recursivamente 
                        primeros_del_simbolo = calcular_primeros_rec(symbol)
                        #regla 2b: restando epsilon
                        primeros[simbolo].update(primeros_del_simbolo - {'ε'})
                        if 'ε' not in primeros_del_simbolo:
                            break
                        #regla 2c: n=1
                        if i == len(produccion) - 1:
                            primeros[simbolo].add('ε')
            
            return primeros[simbolo]
        
        # Calcular primeros para cada símbolo de la gramática
        for simbolo in gramatica:
            calcular_primeros_rec(simbolo)
        
        return primeros
        
    def calcular_siguientes(gramatica, primeros, simbolo_inicial):

        no_terminales = set(gramatica.keys())
        siguientes = {no_terminal: set() for no_terminal in no_terminales}

        # Regla 1: Si A es el símbolo inicial de la gramática, añadir $ a SIGUIENTES(A)
        siguientes[simbolo_inicial].add('$')
        
        # Función auxiliar para calcular los siguientes de un no terminal
        def calcular_siguientes_rec(no_terminal):
            for nt, producciones in gramatica.items():
                for produccion in producciones:
                    if no_terminal in produccion:
                        index = produccion.index(no_terminal)
                        # Regla 2a: Añadir PRIMEROS(β) - {ε} a SIGUIENTES(A)
                        siguiente_simbolo = produccion[index + 1] if index < len(produccion) - 1 else None
                        if siguiente_simbolo is not None:
                            if siguiente_simbolo in no_terminales:
                                siguientes[no_terminal].update(primeros[siguiente_simbolo] - {'ε'})
                            else:
                                siguientes[no_terminal].add(siguiente_simbolo)
                        # Regla 2b: Si ε está en PRIMEROS(β) o β = ε, entonces añadir SIGUIENTES(B) a SIGUIENTES(A)
                    
                        if (siguiente_simbolo is None) or ('ε' in primeros.get(siguiente_simbolo, [])):
                            siguientes[no_terminal].update(siguientes[nt])
        
        # Iterar hasta que no se puedan añadir más símbolos a los siguientes
        cambios = True
        while cambios:
            cambios = False
            for no_terminal in no_terminales:
                antes = set(siguientes[no_terminal])
                calcular_siguientes_rec(no_terminal)
                if antes != siguientes[no_terminal]:
                    cambios = True

        return siguientes
        
    def calcular_prediccion(gramatica, primeros, siguientes, no_terminal):
        prediccion = set()
        
        for regla in gramatica[no_terminal]:
            prediccion.add(no_terminal+'->'+''.join(regla))
        predicciones = {predicc: set() for predicc in prediccion}
        
        for produccion in gramatica[no_terminal]:
            predic = no_terminal+'->'+''.join(produccion)
            
            if produccion[0] in gramatica.keys():
                predicciones[predic] = calcular_prediccion_rec(predicciones, produccion, predic, primeros, 0)
            else:
                if produccion[0] =='ε':
                    predicciones[predic].update(siguientes[no_terminal])
                else:
                    predicciones[predic]= produccion[0]

        return predicciones
        
    def calcular_prediccion_rec(predicciones, produccion, predic, primeros, it_regla):
        if (len(produccion)) != it_regla:
            if produccion[it_regla] in gramatica.keys():
                predicciones[predic].update(primeros[produccion[it_regla]]- {'ε'})
                if 'ε' in primeros[produccion[it_regla]]:
                    return calcular_prediccion_rec(predicciones, produccion, predic, primeros, it_regla+1)
                else:
                    return predicciones[predic]
            else:
                
                predicciones[predic].add(produccion[it_regla])
                return predicciones[predic]
        else:
            return predicciones[predic]
        
    #Llamado a Primer Taller
    print("Conjuntos de Primeros, Siguientes y Predicción: \n")

    primeros = calcular_primeros(gramatica)
    for simbolo, primeros_simbolo in primeros.items():
        print(f'PRIMEROS({simbolo}): {primeros_simbolo}')
    print(" ")

    siguientes = calcular_siguientes(gramatica, primeros, simboloInicial)
    for no_terminal, conjunto_siguientes in siguientes.items():
        print(f'SIGUIENTES({no_terminal}): {conjunto_siguientes}')
    print(" ")

    """
    for no_terminal in gramatica.keys():
        predicciones = calcular_prediccion(gramatica, primeros, siguientes, no_terminal)
        for produccion, conjunto_predicciones in predicciones.items():
            print(f'{produccion}: {conjunto_predicciones}')
    print(" ") """

    # Inicializar un diccionario vacío para almacenar todas las predicciones
    todas_predicciones = {}
    for no_terminal in gramatica.keys():
        predicciones = calcular_prediccion(gramatica, primeros, siguientes, no_terminal)
        for produccion, conjunto_predicciones in predicciones.items():
            # Verificar si la clave ya existe en el diccionario
            if produccion in todas_predicciones:
                # Si la clave existe, extender el valor existente con las nuevas predicciones
                todas_predicciones[produccion].extend(conjunto_predicciones)
            else:
                # Si la clave no existe, crear una nueva entrada en el diccionario
                todas_predicciones[produccion] = conjunto_predicciones

    # Imprimir el diccionario completo de todas las predicciones
    for produccion, conjunto_predicciones in todas_predicciones.items():
        print(f'{produccion}: {conjunto_predicciones}')


    return todas_predicciones
            


"""
def main():
    # Ejemplo de lista de tokens para analizar
    #(ident)
    #(((ident)))
    tokens = [
              ('tk_left_parenthesis', 1, 4),
              ('tk_left_parenthesis', 2, 4),
              ('tk_left_parenthesis', 3, 4),
              ('Id', 'a', 3, 2),  
              ('tk_plus', 1, 2),  
              ('Id', 'a', 3, 2),  
              ('tk_slash', 1, 2),  
              ('tk_left_parenthesis', '(', 3, 4),
              ('Id', 'a', 3, 2), 
              ('tk_minus', 1, 2),  
              ('Id', 'ident', 3, 2), 
            
              ('tk_right_parenthesis', 1, 13),
              ('tk_right_parenthesis', 2, 13),
              ('tk_right_parenthesis', 3, 13),
              ('$', '$', 6, 13)]
    

    
    # Crear el analizador sintáctico y comenzar el análisis
    analizador = AnalizadorSintactico(tokens)
    analizador.analizar()

if __name__ == "__main__":
    main() 
"""
