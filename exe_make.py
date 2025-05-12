import os
import sys
import subprocess
import shutil
from pathlib import Path

def create_standalone_exe(python_script_path, output_dir=None, onefile=True, console=True, icon_path=None, additional_data=None, upx_dir=None):
    try:
        import PyInstaller
    except ImportError:
        print("Установка PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    args = [sys.executable, "-m", "PyInstaller"]
    
    if onefile:
        args.append("--onefile")
    if not console:
        args.append("--windowed")
    if icon_path:
        args.extend(["--icon", str(icon_path)])
    if output_dir:
        args.extend(["--distpath", str(output_dir)])
    if upx_dir:
        args.extend(["--upx-dir", str(upx_dir)])
    
    if additional_data:
        for src, dest in additional_data:
            args.extend(["--add-data", f"{src}{os.pathsep}{dest}"])
    
    args.append(str(python_script_path))
    
    print("Создание EXE-файла...")
    print("Команда:", " ".join(args))
    
    subprocess.check_call(args)
    
    script_name = Path(python_script_path).stem
    exe_name = f"{script_name}.exe"
    
    if onefile and output_dir:
        exe_path = Path(output_dir) / exe_name
    elif onefile:
        exe_path = Path("dist") / exe_name
    else:
        exe_path = Path(output_dir if output_dir else "dist") / script_name / exe_name
    
    print(f"\nEXE-файл успешно создан: {exe_path}")
    return str(exe_path)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Создание автономного EXE из Python-скрипта")
    parser.add_argument("script", help="Путь к Python-скрипту")
    parser.add_argument("--output", help="Выходной каталог", default=None)
    parser.add_argument("--onefile", help="Создать один EXE-файл", action="store_true", default=True)
    parser.add_argument("--console", help="Консольное приложение", action="store_true", default=True)
    parser.add_argument("--icon", help="Путь к иконке (.ico)", default=None)
    parser.add_argument("--upx", help="Путь к UPX для сжатия", default=None)
    
    args = parser.parse_args()
    
    create_standalone_exe(
        python_script_path=args.script,
        output_dir=args.output,
        onefile=args.onefile,
        console=args.console,
        icon_path=args.icon,
        upx_dir=args.upx
    )