import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_PATH = "../db/goodreads-db.sqlite"

class GoodreadsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Goodreads CRUD Interface")
        self.geometry("1000x600")
        self.configure(bg="#f4f4f4")
        self.resizable(False, False)

        self.conn = self.connect_db()
        self.current_table = tk.StringVar()
        self.table_names = self.get_tables()
        self.create_widgets()

    def connect_db(self):
        try:
            return sqlite3.connect(DB_PATH)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"No se pudo conectar: {e}")
            self.quit()

    def get_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [row[0] for row in cursor.fetchall()]

    def create_widgets(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
        style.configure("TButton", font=("Segoe UI", 10, "bold"))

        top_frame = tk.Frame(self, bg="#f4f4f4")
        top_frame.pack(fill=tk.X, pady=10, padx=10)

        tk.Label(top_frame, text="Tabla:", bg="#f4f4f4").pack(side=tk.LEFT)
        ttk.Combobox(top_frame, values=self.table_names, textvariable=self.current_table, state="readonly").pack(side=tk.LEFT, padx=10)
        tk.Button(top_frame, text="Cargar", command=self.load_table).pack(side=tk.LEFT)

        self.search_var = tk.StringVar()
        tk.Entry(top_frame, textvariable=self.search_var, width=30).pack(side=tk.RIGHT, padx=10)
        tk.Button(top_frame, text="Buscar", command=self.search_records).pack(side=tk.RIGHT)

        self.tree = ttk.Treeview(self)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        bottom_frame = tk.Frame(self, bg="#f4f4f4")
        bottom_frame.pack(pady=5)

        tk.Button(bottom_frame, text="Agregar", command=self.add_record).pack(side=tk.LEFT, padx=5)
        tk.Button(bottom_frame, text="Actualizar", command=self.update_record).pack(side=tk.LEFT, padx=5)
        tk.Button(bottom_frame, text="Eliminar", command=self.delete_record).pack(side=tk.LEFT, padx=5)

    def load_table(self):
        table = self.current_table.get()
        if not table:
            messagebox.showwarning("Aviso", "Selecciona una tabla primero.")
            return
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            self.tree.delete(*self.tree.get_children())
            self.tree["columns"] = columns
            self.tree["show"] = "headings"
            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, anchor=tk.CENTER, stretch=True, width=150)
            for row in rows:
                self.tree.insert("", "end", values=row)
        except sqlite3.Error as e:
            messagebox.showerror("Error", str(e))

    def search_records(self):
        search_term = self.search_var.get()
        if not search_term:
            self.load_table()
            return
        table = self.current_table.get()
        cursor = self.conn.cursor()
        try:
            cursor.execute(f"PRAGMA table_info({table});")
            cols = [col[1] for col in cursor.fetchall()]
            like_query = " OR ".join([f"{col} LIKE ?" for col in cols])
            params = [f"%{search_term}%"] * len(cols)
            cursor.execute(f"SELECT * FROM {table} WHERE {like_query}", params)
            results = cursor.fetchall()
            self.tree.delete(*self.tree.get_children())
            for row in results:
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Buscar", f"Error en búsqueda: {e}")

    def add_record(self):
        table = self.current_table.get()
        if not table:
            messagebox.showwarning("Agregar", "Selecciona una tabla primero.")
            return

        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA table_info({table});")
        columns_info = cursor.fetchall()

        # Filtrar columnas que NO son autoincrement (pk = 1 y tipo INTEGER)
        editable_columns = [col[1] for col in columns_info if not (col[5] == 1 and col[2].upper() == "INTEGER")]

        popup = tk.Toplevel(self)
        popup.title("Agregar Registro")
        popup.geometry("400x400")
        entries = {}

        for i, col in enumerate(editable_columns):
            tk.Label(popup, text=col).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = tk.Entry(popup, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[col] = entry

        def submit():
            values = [entries[col].get() for col in editable_columns]
            placeholders = ", ".join(["?"] * len(editable_columns))
            try:
                cursor.execute(f"INSERT INTO {table} ({', '.join(editable_columns)}) VALUES ({placeholders})", values)
                self.conn.commit()
                popup.destroy()
                self.load_table()
            except Exception as e:
                messagebox.showerror("Error al insertar", str(e))

        tk.Button(popup, text="Guardar", command=submit).grid(row=len(editable_columns), columnspan=2, pady=15)


        tk.Button(popup, text="Guardar", command=submit).grid(row=len(columns), columnspan=2, pady=15)

    def update_record(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Actualizar", "Selecciona un registro.")
            return

        table = self.current_table.get()
        record = self.tree.item(selected[0])["values"]
        columns = self.tree["columns"]
        pk_column = columns[0]

        # Obtener metadatos para identificar el campo autoincremental
        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA table_info({table});")
        columns_info = cursor.fetchall()

        # Detectar columnas editables (excluir PK autoincremental)
        editable_columns = [col[1] for col in columns_info if not (col[5] == 1 and col[2].upper() == "INTEGER")]
        pk_value = record[0]

        popup = tk.Toplevel(self)
        popup.title("Actualizar Registro")
        popup.geometry("400x400")
        entries = {}

        for i, col in enumerate(columns):
            tk.Label(popup, text=col).grid(row=i, column=0, padx=10, pady=5, sticky="e")

            entry = tk.Entry(popup, width=30)
            entry.insert(0, record[i])
            entry.grid(row=i, column=1, padx=10, pady=5)

            if col == pk_column:
                entry.configure(state="disabled")  # hacer el ID no editable

            entries[col] = entry

        def submit():
            updated_values = [entries[col].get() for col in editable_columns]
            update_query = ", ".join([f"{col} = ?" for col in editable_columns])
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    f"UPDATE {table} SET {update_query} WHERE {pk_column} = ?",
                    updated_values + [pk_value]
                )
                self.conn.commit()
                popup.destroy()
                self.load_table()
            except Exception as e:
                messagebox.showerror("Error al actualizar", str(e))

        tk.Button(popup, text="Guardar cambios", command=submit).grid(row=len(columns), columnspan=2, pady=15)


    def delete_record(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Eliminar", "Selecciona un registro.")
            return

        table = self.current_table.get()
        record = self.tree.item(selected[0])["values"]
        pk_column = self.tree["columns"][0]
        pk_value = record[0]

        confirm = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar el registro con {pk_column} = {pk_value}?"
        )

        if not confirm:
            return  # El usuario canceló

        try:
            cursor = self.conn.cursor()
            cursor.execute(f"DELETE FROM {table} WHERE {pk_column} = ?", (pk_value,))
            self.conn.commit()
            self.tree.delete(selected[0])
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e))


if __name__ == "__main__":
    app = GoodreadsApp()
    app.mainloop()
