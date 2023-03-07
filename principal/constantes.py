class Opciones:
    def __init__(self):
        pass
    def genero(self):
        GENERO= (('M', 'Masculino'),('F', 'Femenino'),)
        return GENERO
    def tipo_licencia(self):
        TIPO_LICENCIA=(('A','Tipo A'),('B','Tipo B'),('C','Tipo C'),('D','Tipo D'),('E','Tipo E'),('F','Tipo F'),
                       ('G','Tipo G'),
                       ('A1','Tipo A1'),
                       ('C1','Tipo C1'))
        return TIPO_LICENCIA

    def grupo_sanguineo(self):
        GRUPO_SANGUINEO=(('A+','Tipo A+'),('B+','Tipo B+'),('O+','Tipo O+'),('AB+','Tipo AB+'),('A-','Tipo A-'),
                         ('B-','Tipo B-'),('O-','Tipo O-'),('AB-','Tipo AB-'))
        return GRUPO_SANGUINEO

    def ruta(self):
        RUTA=(('V - G','Vinces - Guayaquil'),('G - V', 'Guayaquil - Vinces'))
        return RUTA