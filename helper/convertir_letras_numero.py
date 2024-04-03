import re

class ConvertirMonedaCadena:

    def __init__(self):
        self.UNIDADES = ["", "uno ", "dos ", "tres ", "cuatro ", "cinco ", "seis ", "siete ", "ocho ", "nueve "]
        self.DECENAS = ["diez ", "once ", "doce ", "trece ", "catorce ", "quince ", "dieciseis ",
                        "diecisiete ", "dieciocho ", "diecinueve", "veinte ", "treinta ", "cuarenta ",
                        "cincuenta ", "sesenta ", "setenta ", "ochenta ", "noventa "]
        self.CENTENAS = ["", "ciento ", "doscientos ", "trecientos ", "cuatrocientos ", "quinientos ", "seiscientos ",
                         "setecientos ", "ochocientos ", "novecientos "]

    def convertir(self, numero: str, mayusculas: bool, moneda: str):
        literal = ""
        parte_decimal = ""

        # si el numero utiliza (.) en lugar de (,) -> se reemplaza
        numero = numero.replace(".", ",")

        # si el numero no tiene parte decimal, se le agrega ,00
        if ',' not in numero:
            numero += ",00"

        # se valida formato de entrada -> 0,00 y 999 999 999,00
        pattern = re.compile(r'\d{1,9},\d{1,2}')
        match = pattern.match(numero)

        if match:
            # se divide el numero 0000000,00 -> entero y decimal
            num = numero.split(',')

            # se da formato al numero decimal
            parte_decimal = "con " + num[1] + "/100 " + moneda

            # se convierte el numero a literal
            if int(num[0]) == 0:  # si el valor es cero
                literal = "cero "
            elif int(num[0]) > 999999:  # si es millon
                literal = self.get_millones(num[0])
            elif int(num[0]) > 999:  # si es miles
                literal = self.get_miles(num[0])
            elif int(num[0]) > 99:  # si es centena
                literal = self.get_centenas(num[0])
            elif int(num[0]) > 9:  # si es decena
                literal = self.get_decenas(num[0])
            else:  # sino unidades -> 9
                literal = self.get_unidades(num[0])

            # devuelve el resultado en mayúsculas o minúsculas
            if mayusculas:
                return (literal + parte_decimal).upper()
            else:
                return literal + parte_decimal
        else:  # error, no se puede convertir
            return "Sin valor"

    def get_unidades(self, numero):   # 1 - 9
        # si tuviera algún 0 antes se lo quita -> 09 = 9 o 009=9
        num = numero[-1]
        return self.UNIDADES[int(num)]

    def get_decenas(self, num):  # 99
        n = int(num)
        if n < 10:  # para casos como -> 01 - 09
            return self.get_unidades(num)
        elif n > 19:  # para 20...99
            u = self.get_unidades(num)
            if u == "":  # para 20,30,40,50,60,70,80,90
                return self.DECENAS[int(num[0]) + 8]
            else:
                return self.DECENAS[int(num[0]) + 8] + "y " + u
        else:  # numeros entre 11 y 19
            return self.DECENAS[n - 10]

    def get_centenas(self, num):  # 999 o 099
        if int(num) > 99:  # es centena
            if int(num) == 100:  # caso especial
                return "cien "
            else:
                return self.CENTENAS[int(num[0])] + self.get_decenas(num[1:])
        else:  # por Ej. 099
            # se quita el 0 antes de convertir a decenas
            return self.get_decenas(str(int(num)))

    def get_miles(self, numero):  # 999 999
        # obtiene las centenas
        c = numero[-3:]
        # obtiene los miles
        m = numero[:-3]
        # se comprueba que miles tenga valor entero
        if int(m) > 0:
            n = self.get_centenas(m)
            return n + "mil " + self.get_centenas(c)
        else:
            return self.get_centenas(c)

    def get_millones(self, numero):  # 000 000 000
        # se obtiene los miles
        miles = numero[-6:]
        # se obtiene los millones
        millon = numero[:-6]
        n = self.get_centenas(millon) + "millones " if len(millon) > 1 else self.get_unidades(millon) + "millon "
        return n + self.get_miles(miles)