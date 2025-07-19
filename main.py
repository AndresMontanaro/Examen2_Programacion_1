import ejercicio1, ejercicio2, time

class ControlExamen:

    @classmethod
    def menu(cls) -> None:

        while True:
            print("\n--- EXAMEN 2 ---")
            print("Seleccione una opción:")
            print("1. Acceder al ejercicio 1")
            print("2. Acceder al ejercicio 2")
            print("3. Salir")
            
            opcion = input("\nIngrese su opción: ")
            
            match opcion:
                case '1':
                    while True:
                        print("\n--- EJERCICIO 1 ---")
                        print("Seleccione una opción:")
                        print("1. Descubrir las palabras ocultas en el archivo Excel")
                        print("2. Buscar las palabras ocultas en la sopa de letras")
                        print("3. Salir del submenu")
                        
                        sub_opcion = input("\nIngrese su opción: ")
                        
                        if sub_opcion == '1' or sub_opcion == '2':
                            cls.__acceder_ejercicio_1(sub_opcion)
                            input("\n\nPresione Enter para continuar...")
                        elif sub_opcion == '3':
                            print("\nSaliendo del submenu...")
                            time.sleep(1)
                            break
                        else:
                            print("\nOpción no válida, intente de nuevo.")

                case '2':
                    while True:

                        funciones = [(valor.__name__, valor) for valor in ejercicio2.PalabrasEjercicio.__dict__.values() 
                                         if callable(valor)]
                        
                        print("\n--- EJERCICIO 2 ---")
                        print("Seleccione una opción:")
                        print("1. Ver las operaciones disponibles")
                        print("2. Mostrar todos los resultados de las operaciones")
                        print("3. Salir del submenu")
                        
                        sub_opcion = input("\nIngrese su opción: ")
                                                
                        if sub_opcion == '1':
                            print("\nOperaciones disponibles:")
    
                            for idx, funcion in enumerate(funciones, start=1):
                                print(f"{idx}. {str(funcion[0]).replace('_', ' ').capitalize()}")

                            tri_opcion = input("\nSeleccione una operación (1-10): ")

                            if 1 <= int(tri_opcion) <= len(funciones):
                                funcion = funciones[int(tri_opcion) - 1][1]
                                
                                cls.__acceder_ejercicio_2(funciones=[funcion])

                                input("\nPresione Enter para continuar...")

                            else:
                                print("\nOpción no válida, intente de nuevo.")

                        elif sub_opcion == '2':
                            ejecutables_funciones = [valor[1] for valor in funciones]

                            cls.__acceder_ejercicio_2(funciones=ejecutables_funciones)

                            input("\nPresione Enter para continuar...")

                        elif sub_opcion == '3':
                            print("\nSaliendo del submenu...")
                            time.sleep(1)
                            break
                        else:
                            print("\nOpción no válida, intente de nuevo.")

                case '3':
                    print("Saliendo del programa...")
                    time.sleep(2)
                    return
                case _:
                    print("Opción no válida, intente de nuevo.")

    @classmethod
    def __acceder_ejercicio_1(cls, opcion) -> None:
        
        def descubrir_palabras_ocultas() -> None:
            try:
                df_palabras = ejercicio1.ArchivoExcel.leer_palabras()
                palabras = ejercicio1.AdministrarExcel.recoger_palabras(df_palabras)

                print("\nPALABRAS ENCONTRADAS: ", end='')
                for palabra in palabras:
                    print(palabra, end=', ')

            except Exception as e:
                print(f"\nError al descubrir palabras: {e}")

        def buscar_palabras_en_sopa() -> None:
            try:
                df_palabras = ejercicio1.ArchivoExcel.leer_palabras()
                palabras = ejercicio1.AdministrarExcel.recoger_palabras(df_palabras)

                df_sopa = ejercicio1.ArchivoExcel.leer_sopa()

                print("\nPalabra\t Dirección\t Fila\t Columna Inicio Final".upper())

                for palabra in palabras:
                    buscador = ejercicio1.BuscarPalabrasExcel(df_sopa)
                    resultado = buscador.buscar_palabra(palabra)

                    print("---------------------------------------------------------")
                    if resultado:
                        print(f"{resultado['palabra']}\t {resultado['dirección']}\t {resultado['fila']}\t "
                              f"{resultado['columna']}\t {resultado['comienzo']}\t{resultado['final']}")

            except Exception as e:
                print(f"\nError al buscar palabras en la sopa: {e}")

        if opcion == '1':
            descubrir_palabras_ocultas()
        else:
            buscar_palabras_en_sopa()

    @classmethod
    def __acceder_ejercicio_2(cls, funciones) -> None:
        
        for funcion in funciones:
            try:
                db = ejercicio2.SQLServerConnection()
                repositorio = ejercicio2.PalabrasRepositorio(db)
                registros = repositorio.obtener_palabras()

                resultado = funcion(registros)

                if resultado:
                    print(f"\nResultados de la operación '{funcion.__name__}':")

                    print("\nTexto\t\t Indice_Tabla \t Posicion_Cadena")
                    print("---------------------------------------------------------")
                            
                    for texto, idx, pos in resultado:
                            print(f"'{texto}'\t\t {idx}\t\t {pos if pos is not None else 'N/A'}")

                    time.sleep(2)

                else:
                    print(f"\nNo se encontraron resultados para la operación '{funcion.__name__}'.")

            except Exception as e:
                print(f"\nError al ejecutar la operación '{funcion.__name__}': {e}")

            finally:
                repositorio.cerrar_conexion()

if __name__ == "__main__":
    ControlExamen.menu()