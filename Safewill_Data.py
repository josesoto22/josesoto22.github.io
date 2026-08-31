import csv
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import openpyxl

try:
    import ctypes
    myappid = 'safewill.data.unificador.v1.0'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass


# Función indispensable para encontrar el icono DENTRO del .exe
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class CSVFixerAndMergerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Safewill Data")
        self.root.geometry("580x480")
        self.root.resizable(False, False)

        # Cargar el icono usando la función resource_path
        icono_path = resource_path("icono.ico")
        if os.path.exists(icono_path):
            self.root.iconbitmap(icono_path)

        self.file_paths = []
        self.cleaned_files_data = []

        self.create_widgets()
class CSVFixerAndMergerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Safewill Data")
        self.root.geometry("580x480")
        self.root.resizable(False, False)

        self.file_paths = []
        self.cleaned_files_data = []

        self.create_widgets()

    def create_widgets(self):
        tk.Label(
            self.root,
            text="Unificador de CSV",
            font=("Helvetica", 14, "bold"),
        ).pack(pady=12)

        file_frame = tk.Frame(self.root)
        file_frame.pack(fill="x", padx=20, pady=5)

        self.btn_select = tk.Button(
            file_frame,
            text="1. Cargar archivos CSV",
            command=self.load_csvs,
            bg="#2196F3",
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=10,
        )
        self.btn_select.pack(side="left")

        self.lbl_file = tk.Label(
            file_frame,
            text="Sin archivos seleccionados",
            fg="gray",
            anchor="w",
            wraplength=360,
            justify="left",
        )
        self.lbl_file.pack(side="left", fill="x", expand=True, padx=10)

        info_frame = tk.LabelFrame(
            self.root,
            text="Uso",
            font=("Helvetica", 9, "bold"),
            padx=10,
            pady=8,
        )
        info_frame.pack(fill="x", padx=20, pady=10)

        self.lbl_info = tk.Label(
            info_frame,
            text="• Selecciona múltiples archivos .csv.\n"
                 "• Elija si quiere los datos compretos o promediados.\n"
                 "• Guarde el archivo en formato .csv o .xlsx.",
            font=("Helvetica", 9),
            justify="left",
        )
        self.lbl_info.pack(anchor="w")

        # OPCIÓN DE PROMEDIO POR HORA
        self.var_promediar = tk.BooleanVar(value=False)
        self.chk_promedio = tk.Checkbutton(
            self.root,
            text="Promediar datos por hora (ej. Hora 11, Hora 12...)",
            variable=self.var_promediar,
            font=("Helvetica", 10, "bold"),
            fg="#1565C0",
        )
        self.chk_promedio.pack(pady=5)

        # Opciones de guardado
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill="x", padx=20, pady=10)

        self.btn_save_csv = tk.Button(
            btn_frame,
            text="Guardar archivos unidos como CSV (.csv)",
            command=self.save_csv,
            bg="#009688",
            fg="white",
            font=("Helvetica", 10, "bold"),
            pady=8,
            state="disabled",
        )
        self.btn_save_csv.pack(side="left", expand=True, fill="x", padx=5)

        self.btn_save_excel = tk.Button(
            btn_frame,
            text="Guardar archivos unidos como Excel (.xlsx)",
            command=self.save_excel,
            bg="#4CAF50",
            fg="white",
            font=("Helvetica", 10, "bold"),
            pady=8,
            state="disabled",
        )
        self.btn_save_excel.pack(side="left", expand=True, fill="x", padx=5)

        self.lbl_status = tk.Label(
            self.root, text="", fg="green", font=("Helvetica", 10, "italic")
        )
        self.lbl_status.pack(pady=5)

    def _parse_and_clean_value(self, val):
        """Corrige fechas YY-M-D o YYYY-M-D a DD/MM/YYYY y convierte números."""
        val = str(val).strip()

        subparts = val.split("-")
        if len(subparts) == 3 and all(p.isdigit() for p in subparts):
            yy, mm, dd = subparts
            yyyy = f"20{yy}" if len(yy) == 2 else yy
            return f"{dd.zfill(2)}/{mm.zfill(2)}/{yyyy}"

        try:
            if "." in val:
                return float(val)
            return int(val)
        except ValueError:
            return val

    def _leer_y_corregir_csv(self, filepath):
        filas = []
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                if not row or any("sep=" in str(celda).lower() for celda in row):
                    continue

                parsed_row = [self._parse_and_clean_value(celda) for celda in row]
                filas.append(parsed_row)
        return filas

    def load_csvs(self):
        files_selected = filedialog.askopenfilenames(
            title="Selecciona los archivos CSV a corregir y unir",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")],
        )
        if not files_selected:
            return

        self.file_paths = files_selected
        nombres = [os.path.basename(f) for f in self.file_paths]
        texto_archivos = f"{len(nombres)} archivos cargados."
        self.lbl_file.config(text=texto_archivos, fg="black")

        try:
            self.cleaned_files_data = [
                self._leer_y_corregir_csv(f) for f in self.file_paths
            ]

            if not any(self.cleaned_files_data):
                messagebox.showerror("Error", "Los archivos seleccionados están vacíos.")
                return

            self.btn_save_csv.config(state="normal")
            self.btn_save_excel.config(state="normal")
            self.lbl_status.config(
                text="¡Archivos cargados correctamente!", fg="#2196F3"
            )

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron procesar los archivos:\n{e}")

    def _extraer_hora_simplificada(self, celda_time):
        """Extrae la hora pura para el cálculo del promedio (ej. '11:09:34' -> '11')"""
        texto = str(celda_time).strip()
        if ":" in texto:
            hora_str = texto.split(":")[0]
            if hora_str.isdigit():
                return str(int(hora_str))
        return texto

    def _procesar_archivo_individual(self, filas, promediar=False):
        """Extrae tipo de sensor, unidad original y filas de datos (promediadas o en crudo intactas)."""
        if not filas:
            return "", "Value", []

        nombre_sensor = ""
        if len(filas[0]) >= 2:
            nombre_sensor = str(filas[0][1]).strip()

        encabezado_unidad = "Value"
        if len(filas) > 1 and len(filas[1]) >= 3:
            encabezado_unidad = str(filas[1][2]).strip()

        datos = filas[2:]

        if promediar:
            grupos = {}
            for fila in datos:
                if len(fila) < 3:
                    continue

                fecha = fila[0]
                hora_simple = self._extraer_hora_simplificada(fila[1])
                valor = fila[2] if isinstance(fila[2], (int, float)) else None

                clave = (fecha, hora_simple)

                if clave not in grupos:
                    grupos[clave] = []

                if valor is not None:
                    grupos[clave].append(valor)

            filas_resultado = []
            for (fecha, hora_simple), valores in grupos.items():
                promedio = round(sum(valores) / len(valores), 2) if valores else ""
                filas_resultado.append((fecha, hora_simple, promedio))
            return nombre_sensor, encabezado_unidad, filas_resultado

        else:
            # DATOS CRUDOS INTACTOS (mantiene todas las filas y horas exactas)
            filas_resultado = []
            for fila in datos:
                if len(fila) >= 3:
                    fecha = fila[0]
                    hora_exacta = str(fila[1]).strip()
                    valor = fila[2]
                    filas_resultado.append((fecha, hora_exacta, valor))
            return nombre_sensor, encabezado_unidad, filas_resultado

    def _obtener_filas_unidas(self):
        """Une los archivos compartiendo las primeras 2 columnas (Date y Time)."""
        if not self.cleaned_files_data:
            return []

        promediar = self.var_promediar.get()
        sensores = []
        unidades = []
        datos_archivos = []

        for f in self.cleaned_files_data:
            sensor, unidad, datos = self._procesar_archivo_individual(f, promediar=promediar)
            sensores.append(sensor)
            unidades.append(unidad)
            datos_archivos.append(datos)

        # Fila 1: ["", "Sensor Type", "SO2", "NO2", "O3", ...]
        header_row1 = ["", "Sensor Type"] + sensores

        # Fila 2: ["Date", "Time", "Value/ppb", "Value/%RH", ...]
        header_row2 = ["Date", "Time"] + unidades

        # Alinear todas las lecturas por su clave única (Fecha, Hora)
        fechas_horas_ordenadas = []
        tabla_map = {}

        for idx_archivo, datos in enumerate(datos_archivos):
            for fecha, hora, valor in datos:
                clave = (fecha, hora)
                if clave not in tabla_map:
                    tabla_map[clave] = [""] * len(datos_archivos)
                    fechas_horas_ordenadas.append(clave)
                tabla_map[clave][idx_archivo] = valor

        # Construir tabla final
        filas_finales = [header_row1, header_row2]
        for fecha, hora in fechas_horas_ordenadas:
            valores_sensores = tabla_map[(fecha, hora)]
            filas_finales.append([fecha, hora] + valores_sensores)

        return filas_finales

    def save_csv(self):
        save_path = filedialog.asksaveasfilename(
            title="Guardar archivo unido como CSV",
            defaultextension=".csv",
            initialfile="Datos.csv",
            filetypes=[("Archivos CSV", "*.csv")],
        )
        if not save_path:
            return

        try:
            filas_unidas = self._obtener_filas_unidas()

            with open(save_path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f, delimiter=";")
                for fila in filas_unidas:
                    writer.writerow(fila)

            self.lbl_status.config(text="¡CSV guardado con éxito!", fg="green")
            messagebox.showinfo("Éxito", f"Archivo guardado en:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo CSV:\n{e}")

    def save_excel(self):
        save_path = filedialog.asksaveasfilename(
            title="Guardar archivo unido como Excel",
            defaultextension=".xlsx",
            initialfile="unido.xlsx",
            filetypes=[("Libro de Excel", "*.xlsx")],
        )
        if not save_path:
            return

        try:
            filas_unidas = self._obtener_filas_unidas()

            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Datos Unidos"

            for fila in filas_unidas:
                ws.append(fila)

            for col in ws.columns:
                max_len = max(len(str(cell.value or "")) for cell in col)
                col_letter = openpyxl.utils.get_column_letter(col[0].column)
                ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

            wb.save(save_path)
            self.lbl_status.config(text="¡Excel guardado con éxito!", fg="green")
            messagebox.showinfo("Éxito", f"Archivo Excel guardado en:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo Excel:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CSVFixerAndMergerApp(root)
    root.mainloop()