import pandas as pd, openpyxl
                
class ArchivoExcel:

    @staticmethod
    def leer_sopa() -> pd.DataFrame:
        try:
            df = pd.read_excel("Examen2_AndresMontanaro\\Excel\\Examen2.xlsx", 
                               sheet_name="Sopa",
                               skiprows=4,
                               usecols="E:N",
                               nrows=10,
                               engine='openpyxl')
            return df
        except Exception as e:
            print(f"Error al tratar de leer el archivo Excel: {e}")
            return None
        
    @staticmethod
    def leer_palabras() -> pd.DataFrame:
        try:
            df = pd.read_excel("Examen2_AndresMontanaro\\Excel\\Examen2.xlsx", 
                               sheet_name="Palabras",
                               usecols=(0,),
                               engine='openpyxl')
            return df
        except Exception as e:
            print(f"Error al tratar de leer el archivo Excel: {e}")
            return None

class AdministrarExcel:

    @staticmethod
    def recoger_palabras(df: pd.DataFrame) -> list[str]:
        return [palabra.lower() for palabra in list(df.columns)[0].split()]

class BuscarPalabrasExcel:

    def __init__(self, df: pd.DataFrame) -> None:
        self.data_frame = df
        self.numero_filas, self.numero_columnas = df.shape

    def __buscar_horizontalmente(self, palabra: str) -> tuple[int, int, int] | None:
        numero_letras = len(palabra)
        for fil in range(self.numero_filas):
            cadena_fila = ''.join(self.data_frame.iloc[fil].tolist())
            cadena_fila_inversa = cadena_fila[::-1]

            idx_fila = cadena_fila.find(palabra)
            if idx_fila != -1:
                return (fil + 1, idx_fila + 1, idx_fila + numero_letras)
            
            idx_fila_inversa = cadena_fila_inversa.find(palabra)
            if idx_fila_inversa != -1:
                return (fil + 1, self.numero_columnas - idx_fila_inversa - numero_letras + 1, self.numero_columnas - idx_fila_inversa)
            
        return None

    def __buscar_verticalmente(self, palabra: str) -> tuple[int, int, int] | None:
        numero_letras = len(palabra)
        for col in range(self.numero_columnas):
            cadena_columna = ''.join(self.data_frame.iloc[:, col].tolist())
            cadena_columna_inversa = cadena_columna[::-1]

            idx_columna = cadena_columna.find(palabra)
            if idx_columna != -1:
                return (col + 1, idx_columna + 1, idx_columna + numero_letras)
            
            idx_columna_inversa = cadena_columna_inversa.find(palabra)
            if idx_columna_inversa != -1:
                return (col + 1, self.numero_columnas - idx_columna_inversa - numero_letras + 1, self.numero_columnas - idx_columna_inversa)
            
        return None

    def buscar_palabra(self, palabra: str) -> dict[str, int | None]:

        resultado = {'palabra': palabra, 'dirección': None, 'fila': None,
                  'columna': None, 'comienzo': None, 'final': None}

        palabra_horizontal = self.__buscar_horizontalmente(palabra)
        
        if palabra_horizontal:
            fila, comienzo, final = palabra_horizontal
            resultado.update({'dirección': 'horizontal', 'fila': fila,
                           'comienzo': comienzo, 'final': final})
            return resultado

        palabra_vertical = self.__buscar_verticalmente(palabra)

        if palabra_vertical:
            columna, comienzo, final = palabra_vertical
            resultado.update({'dirección': 'vertical', 'columna': columna,
                           'comienzo': comienzo, 'final': final})
            return resultado
        
