import os
import subprocess
from abc import ABC, abstractmethod

# ✅ SRP: Cada clase tiene una responsabilidad específica
# ✅ OCP y DIP: Se programan contra abstracciones, no implementaciones concretas

class ScriptManager(ABC):
    @abstractmethod
    def mostrar_codigo(self, ruta_script):
        pass

    @abstractmethod
    def ejecutar_codigo(self, ruta_script):
        pass


class PythonScriptManager(ScriptManager):
    def mostrar_codigo(self, ruta_script):
        ruta_script_absoluta = os.path.abspath(ruta_script)
        try:
            with open(ruta_script_absoluta, 'r') as archivo:
                codigo = archivo.read()
                print(f"\n--- Código de {ruta_script} ---\n")
                print(codigo)
                return codigo
        except FileNotFoundError:
            print("❌ El archivo no se encontró.")
            return None
        except Exception as e:
            print(f"❌ Error al leer el archivo: {e}")
            return None

    def ejecutar_codigo(self, ruta_script):
        try:
            if os.name == 'nt':
                subprocess.Popen(['cmd', '/k', 'python', ruta_script])
            else:
                subprocess.Popen(['xterm', '-hold', '-e', 'python3', ruta_script])
        except Exception as e:
            print(f"❌ Error al ejecutar el código: {e}")


class Menu:
    def __init__(self, gestor: ScriptManager):
        self.gestor = gestor
        self.ruta_base = os.path.dirname(__file__)
        self.unidades = {
            '1': 'Unidad 1',
            '2': 'Unidad 2'
        }

    def mostrar_menu_principal(self):
        while True:
            print("\n📚 Menu Principal - Dashboard POO")
            for key in self.unidades:
                print(f"{key} - {self.unidades[key]}")
            print("0 - Salir")

            eleccion = input("Elige una unidad o '0' para salir: ")
            if eleccion == '0':
                print("👋 Saliendo del programa.")
                break
            elif eleccion in self.unidades:
                ruta_unidad = os.path.join(self.ruta_base, self.unidades[eleccion])
                self.mostrar_sub_menu(ruta_unidad)
            else:
                print("⚠️ Opción no válida. Intenta de nuevo.")

    def mostrar_sub_menu(self, ruta_unidad):
        sub_carpetas = [f.name for f in os.scandir(ruta_unidad) if f.is_dir()]
        while True:
            print("\n📁 Submenú - Selecciona una subcarpeta")
            for i, carpeta in enumerate(sub_carpetas, start=1):
                print(f"{i} - {carpeta}")
            print("0 - Regresar")

            eleccion = input("Elige una subcarpeta o '0' para regresar: ")
            if eleccion == '0':
                break
            else:
                try:
                    eleccion = int(eleccion) - 1
                    if 0 <= eleccion < len(sub_carpetas):
                        ruta_sub = os.path.join(ruta_unidad, sub_carpetas[eleccion])
                        self.mostrar_scripts(ruta_sub)
                    else:
                        print("⚠️ Opción no válida.")
                except ValueError:
                    print("⚠️ Entrada incorrecta. Usa solo números.")

    def mostrar_scripts(self, ruta_sub_carpeta):
        scripts = [f.name for f in os.scandir(ruta_sub_carpeta) if f.is_file() and f.name.endswith('.py')]
        while True:
            print("\n🧩 Scripts disponibles:")
            for i, script in enumerate(scripts, start=1):
                print(f"{i} - {script}")
            print("0 - Regresar")
            print("9 - Menú principal")

            eleccion = input("Elige un script, '0' para regresar o '9' para menú principal: ")
            if eleccion == '0':
                break
            elif eleccion == '9':
                return
            else:
                try:
                    eleccion = int(eleccion) - 1
                    if 0 <= eleccion < len(scripts):
                        ruta_script = os.path.join(ruta_sub_carpeta, scripts[eleccion])
                        codigo = self.gestor.mostrar_codigo(ruta_script)
                        if codigo:
                            ejecutar = input("¿Deseas ejecutarlo? (1: Sí, 0: No): ")
                            if ejecutar == '1':
                                self.gestor.ejecutar_codigo(ruta_script)
                            elif ejecutar == '0':
                                print("✅ Visualización sin ejecución.")
                            else:
                                print("⚠️ Opción inválida.")
                            input("Presiona Enter para continuar...")
                    else:
                        print("⚠️ Opción no válida.")
                except ValueError:
                    print("⚠️ Entrada inválida. Usa solo números.")


# ✅ Ejecución principal del dashboard
if __name__ == "__main__":
    gestor_python = PythonScriptManager()
    menu = Menu(gestor_python)
    menu.mostrar_menu_principal()
