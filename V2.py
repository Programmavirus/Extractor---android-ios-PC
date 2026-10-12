import os
import sys
import zipfile
import shutil
import subprocess
import plistlib
from pathlib import Path

OUT = Path("/storage/emulated/0/Download/Android")


class C:
    R = "\033[91m"
    G = "\033[92m"
    Y = "\033[93m"
    B = "\033[94m"
    M = "\033[95m"
    CY = "\033[96m"
    W = "\033[97m"
    BOLD = "\033[1m"
    END = "\033[0m"


def banner():
    print()
    print(C.CY + C.BOLD + "╔" + "═" * 62 + "╗" + C.END)
    print(C.CY + C.BOLD + "║" + C.END + C.W + C.BOLD +
          "                EXTRACTOR — APK / EXE / IPA                " +
          C.END + C.CY + C.BOLD + "║" + C.END)
    print(C.CY + C.BOLD + "╠" + "═" * 62 + "╣" + C.END)
    print(C.CY + C.BOLD + "║" + C.END + " " * 23 + C.M + C.BOLD +
          "Made by: @tryleakq" + C.END + " " * 24 +
          C.CY + C.BOLD + "║" + C.END)
    print(C.CY + C.BOLD + "╠" + "═" * 62 + "╣" + C.END)
    print(C.CY + C.BOLD + "║" + C.END +
          C.G + "  [1]" + C.END + "  APK  " + C.W + "→ Android" + C.END +
          " " * 33 + C.CY + C.BOLD + "║" + C.END)
    print(C.CY + C.BOLD + "║" + C.END +
          C.Y + "  [2]" + C.END + "  EXE  " + C.W + "→ Windows" + C.END +
          " " * 33 + C.CY + C.BOLD + "║" + C.END)
    print(C.CY + C.BOLD + "║" + C.END +
          C.M + "  [3]" + C.END + "  IPA  " + C.W + "→ iOS" + C.END +
          " " * 37 + C.CY + C.BOLD + "║" + C.END)
    print(C.CY + C.BOLD + "║" + C.END +
          C.B + "  [4]" + C.END + "  " + C.W + "ВСЁ СРАЗУ (APK + EXE + IPA)" + C.END +
          " " * 19 + C.CY + C.BOLD + "║" + C.END)
    print(C.CY + C.BOLD + "║" + C.END +
          C.CY + "  [5]" + C.END + "  " + C.W + "Контакты" + C.END +
          " " * 39 + C.CY + C.BOLD + "║" + C.END)
    print(C.CY + C.BOLD + "║" + C.END +
          C.R + "  [0]" + C.END + "  " + C.W + "Выход" + C.END +
          " " * 47 + C.CY + C.BOLD + "║" + C.END)
    print(C.CY + C.BOLD + "╚" + "═" * 62 + "╝" + C.END)
    print()


def menu():
    while True:
        banner()
        choice = input(C.BOLD + "Выбери: " + C.END).strip()
        if choice == "1":
            apk = ask_path("APK", ".apk")
            if apk:
                extract_apk(apk)
                input(C.Y + "\nEnter..." + C.END)
        elif choice == "2":
            exe = ask_path("EXE", ".exe")
            if exe:
                extract_exe(exe)
                input(C.Y + "\nEnter..." + C.END)
        elif choice == "3":
            ipa = ask_path("IPA", ".ipa")
            if ipa:
                extract_ipa(ipa)
                input(C.Y + "\nEnter..." + C.END)
        elif choice == "4":
            run_all()
            input(C.Y + "\nEnter..." + C.END)
        elif choice == "5":
            contacts()
            input(C.Y + "\nEnter..." + C.END)
        elif choice == "0":
            print(C.Y + "Выход." + C.END)
            return
        else:
            print(C.R + "Неверный выбор." + C.END)
            input("Enter...")


def contacts():
    print()
    print(C.CY + C.BOLD + "═══ КОНТАКТЫ ═══" + C.END)
    print()
    print(C.W + "  Telegram: " + C.END + C.M + C.BOLD + "@tryleakq" + C.END)
    print()


def ask_path(label, ext):
    p = input(C.BOLD + f"Путь к {label} ({ext}): " + C.END).strip().strip('"').strip("'")
    if not p:
        return None
    path = Path(p).expanduser().resolve()
    if not path.exists() or not path.is_file():
        print(C.R + f"  ✗ Нет файла: {path}" + C.END)
        return None
    return path


def progress(i, total, label=""):
    percent = int(i / total * 100) if total else 0
    bar = "█" * (percent // 3) + "░" * (33 - percent // 3)
    print(f"\r  {label} [{bar}] {percent}% ({i}/{total})", end="", flush=True)


def unzip_all(src, dst, label="Распаковка"):
    dst.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(src, "r") as z:
        names = z.namelist()
        total = len(names)
        for i, name in enumerate(names, 1):
            try:
                z.extract(name, dst)
            except Exception:
                pass
            if i % 50 == 0 or i == total:
                progress(i, total, label)
        print()
    return total


def stats(folder):
    files = sum(1 for _ in folder.rglob("*") if _.is_file())
    dirs = sum(1 for _ in folder.rglob("*") if _.is_dir())
    return files, dirs


# ============================================================
# 1. APK
# ============================================================
def extract_apk(apk):
    print()
    print(C.G + C.BOLD + "═══ APK → Android ═══" + C.END)
    print(C.W + f"  Файл: {apk.name}" + C.END)

    dest = OUT / (apk.stem + "_apk")
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)

    raw = dest / "raw"
    unzip_all(apk, raw, "APK")

    full = dest / "full"
    full.mkdir()
    for item in raw.iterdir():
        if item.name == "META-INF":
            continue
        target = full / item.name
        if item.is_dir():
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)

    if shutil.which("apktool"):
        print(C.B + "  apktool..." + C.END)
        subprocess.run(
            ["apktool", "d", "-f", "-o", str(dest / "apktool"), str(apk)],
            capture_output=True
        )

    if shutil.which("jadx"):
        print(C.B + "  jadx..." + C.END)
        subprocess.run(
            ["jadx", "-d", str(dest / "jadx"), "--no-res", str(apk)],
            capture_output=True
        )

    f, d = stats(raw)
    print(C.G + f"  ✓ Готово: {f} файлов, {d} папок" + C.END)
    print(C.W + f"    Путь: {dest}" + C.END)


# ============================================================
# 2. EXE
# ============================================================
def extract_exe(exe):
    print()
    print(C.Y + C.BOLD + "═══ EXE → Windows ═══" + C.END)
    print(C.W + f"  Файл: {exe.name}" + C.END)

    dest = OUT / (exe.stem + "_exe")
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)

    zip_dir = dest / "as_zip"
    is_zip = False
    try:
        with zipfile.ZipFile(exe, "r") as z:
            names = z.namelist()
            if len(names) > 0:
                is_zip = True
                total = len(names)
                zip_dir.mkdir()
                for i, name in enumerate(names, 1):
                    try:
                        z.extract(name, zip_dir)
                    except Exception:
                        pass
                    if i % 50 == 0 or i == total:
                        progress(i, total, "ZIP")
                print()
    except Exception:
        pass

    has_pefile = True
    try:
        import pefile  # noqa
    except ImportError:
        has_pefile = False

    if has_pefile:
        print(C.B + "  PE-инфо..." + C.END)
        try:
            import pefile
            pe = pefile.PE(str(exe))
            with open(dest / "pe_info.txt", "w", encoding="utf-8") as f:
                f.write(f"Machine: {hex(pe.FILE_HEADER.Machine)}\n")
                f.write(f"TimeDateStamp: {pe.FILE_HEADER.TimeDateStamp}\n")
                f.write(f"Subsystem: {pe.OPTIONAL_HEADER.Subsystem}\n")
                f.write(f"ImageBase: {hex(pe.OPTIONAL_HEADER.ImageBase)}\n")
                f.write(f"EntryPoint: {hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint)}\n")
                f.write(f"Sections:\n")
                for s in pe.sections:
                    name = s.Name.decode(errors="replace").rstrip("\x00")
                    f.write(f"  {name}: {s.SizeOfRawData} bytes\n")
                if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
                    f.write(f"\nImports:\n")
                    for entry in pe.DIRECTORY_ENTRY_IMPORT:
                        f.write(f"  {entry.dll.decode(errors='replace')}\n")
            pe.close()
        except Exception as e:
            print(C.R + f"  PE ошибка: {e}" + C.END)

    if is_zip:
        f, d = stats(zip_dir)
        print(C.G + f"  ✓ ZIP: {f} файлов, {d} папок" + C.END)
    else:
        print(C.Y + "  EXE не является ZIP." + C.END)
    print(C.G + f"  ✓ PE-инфо: {'есть' if has_pefile else 'нет pefile'}" + C.END)
    print(C.W + f"    Путь: {dest}" + C.END)


# ============================================================
# 3. IPA
# ============================================================
def extract_ipa(ipa):
    print()
    print(C.M + C.BOLD + "═══ IPA → iOS ═══" + C.END)
    print(C.W + f"  Файл: {ipa.name}" + C.END)

    dest = OUT / (ipa.stem + "_ipa")
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)

    raw = dest / "raw"
    unzip_all(ipa, raw, "IPA")

    plist_out = dest / "Info_decoded"
    plist_out.mkdir()
    found = 0
    for plist_path in raw.rglob("Info.plist"):
        try:
            with open(plist_path, "rb") as f:
                data = plistlib.load(f)
            out = plist_out / (plist_path.parent.name + "_Info.plist")
            with open(out, "wb") as f:
                plistlib.dump(data, f, fmt=plistlib.FMT_XML)
            found += 1
        except Exception:
            pass

    f, d = stats(raw)
    print(C.G + f"  ✓ Готово: {f} файлов, {d} папок" + C.END)
    print(C.G + f"  ✓ Info.plist: {found} декодировано" + C.END)
    print(C.W + f"    Путь: {dest}" + C.END)


# ============================================================
# 4. ВСЁ СРАЗУ
# ============================================================
def run_all():
    print()
    print(C.B + C.BOLD + "═══ ВСЁ СРАЗУ — APK + EXE + IPA ═══" + C.END)
    print(C.W + "Введи три пути. Если файла нет — оставь пустым." + C.END)
    print()

    apk = ask_path("APK", ".apk")
    exe = ask_path("EXE", ".exe")
    ipa = ask_path("IPA", ".ipa")

    if not apk and not exe and not ipa:
        print(C.R + "\nНичего не указано." + C.END)
        return

    OUT.mkdir(parents=True, exist_ok=True)

    print()
    print(C.W + "=" * 62 + C.END)
    print(C.W + "  НАЧАЛО ИЗВЛЕЧЕНИЯ" + C.END)
    print(C.W + "=" * 62 + C.END)

    if apk:
        extract_apk(apk)
    if exe:
        extract_exe(exe)
    if ipa:
        extract_ipa(ipa)

    print()
    print(C.G + C.BOLD + "╔" + "═" * 62 + "╗" + C.END)
    print(C.G + C.BOLD + "║" + C.END + C.W + C.BOLD +
          "                     ВСЁ ГОТОВО                            " +
          C.END + C.G + C.BOLD + "║" + C.END)
    print(C.G + C.BOLD + "╚" + "═" * 62 + "╝" + C.END)
    print()
    print(C.W + f"  Папка: {OUT}" + C.END)
    print()


if __name__ == "__main__":
    try:
        OUT.mkdir(parents=True, exist_ok=True)
        menu()
    except KeyboardInterrupt:
        print()
        print(C.Y + "Прервано." + C.END)
    except Exception as e:
        print()
        print(C.R + f"Ошибка: {e}" + C.END)