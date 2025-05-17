import subprocess
import os

def run_script(description, script_path, cwd):
    print(f"\n==> {description} ({script_path})")
    subprocess.run(["python", script_path], check=True, cwd=cwd)

if __name__ == "__main__":
    try:
        project_root = os.path.dirname(os.path.abspath(__file__))

        run_script("Creando base de datos", "create_db.py", cwd=os.path.join(project_root, "src"))
        run_script("Llenando base de datos", "db_fill.py", cwd=os.path.join(project_root, "src"))
        run_script("Ejecutando la aplicación GUI", "gui_app.py", cwd=os.path.join(project_root, "src"))

    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] El script falló: {e}")
