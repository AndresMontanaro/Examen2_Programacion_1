from pyodbc import *
from abc import ABC, abstractmethod

class DatabaseConnection(ABC):

    @abstractmethod
    def conectar(self):
        pass

    @abstractmethod
    def cerrar(self):
        pass

    @abstractmethod
    def fetch(self, consulta: str):
        pass

class SQLServerConnection(DatabaseConnection):

    def __init__(self) -> None:
        self.conexion = None

    def conectar(self) -> None:
        self.conexion = connect(
            f'DRIVER={{SQL Server}};SERVER=DESKTOP-7264;DATABASE=Examen2;Trusted_Connection=yes;'
        )

    def cerrar(self):
        if self.conexion:
            self.conexion.close()

    def fetch(self, consulta: str) -> list[Row]:
        if not self.conexion:
            raise ConnectionError("No hay conexión establecida.")
        else:
            try:
                with self.conexion.cursor() as cursor:
                    cursor.execute(consulta)
                    return cursor.fetchall()
            except Error as e:
                print(f"Error al ejecutar la consulta: {e}")
                return None

class PalabrasRepositorio:

    def __init__(self, db_conexion: DatabaseConnection) -> None:
        self.db_conexion = db_conexion
        self.db_conexion.conectar()

    def obtener_palabras(self) -> list[Row]:
        consulta = "SELECT texto FROM palabras"
        return self.db_conexion.fetch(consulta)

    def cerrar_conexion(self) -> None:
        self.db_conexion.cerrar()

class PalabrasEjercicio:

    @staticmethod
    def administrar_animal_encerrado(registros: list[Row]) -> list[tuple[str, int]] | None:

        registros_encontrados = []

        for idx_registro, registro in enumerate(registros):
            if 'Gato' in str(registro.texto):
                registros_encontrados.append((str(registro.texto).strip(), idx_registro + 1, None))

        return registros_encontrados if registros_encontrados else None
    
    @staticmethod
    def administrar_lenguaje_en_lower(registros: list[Row]) -> list[tuple[str, int]] | None:

        registros_encontrados = []

        for idx_registro, registro in enumerate(registros):
            if 'py' in str(registro.texto) and str(registro.texto).islower():
                registros_encontrados.append((str(registro.texto).upper(), idx_registro + 1, None))
        
        return registros_encontrados if registros_encontrados else None

    @staticmethod
    def administrar_posible_numero(registros: list[Row]) -> list[tuple[str, int]] | None:

        registros_encontrados = []

        for idx_registro, registro in enumerate(registros):
            if str(registro.texto).isdigit():
                registros_encontrados.append((str(registro.texto), idx_registro + 1, None))

        return registros_encontrados if registros_encontrados else None

    @staticmethod
    def administrar_frase_extraida_agua(registros: list[Row]) -> list[tuple[str, int]] | None:

        registros_encontrados = []

        for idx_registro, registro in enumerate(registros):
            if 'agua' in str(registro.texto):
                parte_extraida = str(registro.texto).split('agua')[1].split()
                registros_encontrados.append((parte_extraida[0], idx_registro + 1, None))

        return registros_encontrados if registros_encontrados else None

    @staticmethod
    def administrar_mezcla_texto_letras(registros: list[Row]) -> list[tuple[str, int]] | None: 

        registros_encontrados = []

        for idx_registro, registro in enumerate(registros):

            if str(registro.texto).isalnum():

                tiene_letras = any(caracter.isalpha() for caracter in str(registro.texto))
                tiene_numeros = any(caracter.isnumeric() for caracter in str(registro.texto))

                if tiene_letras and tiene_numeros:
                    if str(registro.texto).isalpha():
                        registros_encontrados.append((str(registro.texto), idx_registro + 1, None))

        return registros_encontrados if registros_encontrados else None

    @staticmethod
    def administrar_lenguajes_similares(registros: list[Row]) -> list[tuple[str, int]] | None:

        registros_similares = []

        for idx_registro, registro in enumerate(registros):
            if str(registro.texto).lower().startswith('py'):
                registros_similares.append((str(registro.texto), idx_registro + 1, None))

        return registros_similares if registros_similares else None

    @staticmethod
    def administrar_frase_pacifica(registros: list[Row]) -> list[tuple[str, int]] | None:

        registros_encontrados = []

        for idx_registro, registro in enumerate(registros):
           if 'cielo' in str(registro.texto):
                registros_encontrados.append((str(registro.texto).swapcase(), idx_registro + 1, None))
        
        return registros_encontrados if registros_encontrados else None

    @staticmethod
    def administrar_fragmentacion_cadenas(registros: list[Row]) -> list[tuple[str, int, int]] | None:

        registros_encontrados = []

        for idx_registro, registro in enumerate(registros):
            if 'split' in str(registro.texto):
                posicion_cadena = str(registro.texto).find('split')
                if posicion_cadena != -1:
                    registros_encontrados.append((str(registro.texto), idx_registro + 1, posicion_cadena))
                else:
                    registros_encontrados.append((str(registro.texto), idx_registro + 1, -1))

        return registros_encontrados if registros_encontrados else None

    @staticmethod
    def administrar_residuos_al_final(registros: list[Row]) -> list[tuple[str, int, int]] | None:
        
        registros_encontrados = []

        for idx_registro, registro in enumerate(registros):
            registro_original = str(registro.texto)

            if str(registro.texto).rstrip() != registro_original:
                registros_encontrados.append((str(registro.texto).rstrip(), idx_registro + 1, None))

        return registros_encontrados if registros_encontrados else None
    
    @staticmethod
    def administrar_informacion_escondida(registros: list[Row]) -> list[tuple[str, int]] | None:

        registros_encontrados = []  

        for idx_registro, registro in enumerate(registros):
            if 'final' in str(registro.texto):
                registro_convertido = str(registro.texto).lstrip().capitalize()
                registros_encontrados.append((registro_convertido, idx_registro + 1, None))

        return registros_encontrados if registros_encontrados else None
    