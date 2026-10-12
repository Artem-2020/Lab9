import ctypes
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
RUST_SOURCE = ROOT_DIR / "rust" / "speed.rs"
BUILD_DIR = ROOT_DIR / "build"
LIMIT = 100_000
REPEATS = 5


def library_path():
    if sys.platform == "win32":
        return BUILD_DIR / "rust_speed.dll"
    if sys.platform == "darwin":
        return BUILD_DIR / "librust_speed.dylib"
    return BUILD_DIR / "librust_speed.so"


def compile_rust_library():
    BUILD_DIR.mkdir(exist_ok=True)
    output = library_path()
    subprocess.run(
        ["rustc", "--crate-type", "cdylib", "-O", str(RUST_SOURCE), "-o", str(output)],
        check=True,
    )
    return output


def is_prime(number):
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 2
    return True


def python_count_primes(limit):
    count = 0
    for number in range(2, limit + 1):
        if is_prime(number):
            count += 1
    return count


def measure(function, *args, repeats=REPEATS):
    times = []
    result = None
    for _ in range(repeats):
        started_at = time.perf_counter()
        result = function(*args)
        times.append(time.perf_counter() - started_at)
    return result, times


def rust_version():
    try:
        return subprocess.check_output(["rustc", "--version"], text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return "не удалось определить"


def write_report(python_result, python_times, rust_result, rust_times):
    py_best, rs_best = min(python_times), min(rust_times)
    speedup = py_best / rs_best if rs_best else float("inf")
    cpu = platform.processor() or "не определён системой"
    report = f'''# Отчёт по заданию №9: сравнение скорости Python и Rust

## Цель работы
Сравнить время выполнения эквивалентных функций подсчёта простых чисел на Python и Rust.

## Условия эксперимента
- Диапазон: от 2 до {LIMIT} включительно (`limit = 100_000`).
- Число повторов каждой реализации: {REPEATS}.
- Измерение времени: `time.perf_counter()`.
- Итоговое время: минимальное из {REPEATS} измерений.
- Rust скомпилирован оптимизированным компилятором (`rustc -O`, тип библиотеки `cdylib`).
- Измеряется только вызов функции; компиляция Rust выполняется до замеров.

## Среда выполнения
- ОС и архитектура: {platform.platform()}
- Процессор: {cpu}
- Логических CPU: {os.cpu_count() or 'не определено'}
- Python: {platform.python_version()}
- Rust: {rust_version()}

## Результаты

| Показатель | Python | Rust |
|---|---:|---:|
| Найдено простых чисел | {python_result} | {rust_result} |
| Замер 1, сек. | {python_times[0]:.6f} | {rust_times[0]:.6f} |
| Замер 2, сек. | {python_times[1]:.6f} | {rust_times[1]:.6f} |
| Замер 3, сек. | {python_times[2]:.6f} | {rust_times[2]:.6f} |
| Замер 4, сек. | {python_times[3]:.6f} | {rust_times[3]:.6f} |
| Замер 5, сек. | {python_times[4]:.6f} | {rust_times[4]:.6f} |
| Минимальное время, сек. | {py_best:.6f} | {rs_best:.6f} |

**Коэффициент ускорения Rust:** {speedup:.2f}× (отношение минимального времени Python к минимальному времени Rust).

## Вывод
Обе реализации вернули одинаковый результат: {python_result} простых чисел в диапазоне от 2 до {LIMIT}. По минимальному времени в данной среде реализация Rust {'быстрее' if speedup > 1 else 'не быстрее'} реализации Python в {speedup:.2f} раза. Результат относится к данной задаче и указанной среде; его нельзя автоматически переносить на другие алгоритмы и оборудование.
'''
    (ROOT_DIR / "REPORT.md").write_text(report, encoding="utf-8")


def main():
    rust_library = ctypes.CDLL(str(compile_rust_library()))
    rust_count_primes = rust_library.rust_count_primes
    rust_count_primes.argtypes = [ctypes.c_uint32]
    rust_count_primes.restype = ctypes.c_uint32

    python_result, python_times = measure(python_count_primes, LIMIT)
    rust_result, rust_times = measure(rust_count_primes, LIMIT)
    if python_result != rust_result:
        raise RuntimeError(f"Результаты не совпали: Python={python_result}, Rust={rust_result}")

    write_report(python_result, python_times, rust_result, rust_times)
    py_best, rs_best = min(python_times), min(rust_times)
    print(f"Функция: подсчёт простых чисел от 2 до {LIMIT}")
    print(f"Результат обеих реализаций: {python_result}")
    print("Python замеры (сек.): " + ", ".join(f"{t:.6f}" for t in python_times))
    print("Rust замеры (сек.):   " + ", ".join(f"{t:.6f}" for t in rust_times))
    print(f"Минимум Python: {py_best:.6f} сек.")
    print(f"Минимум Rust:   {rs_best:.6f} сек.")
    print(f"Ускорение Rust: {py_best / rs_best:.2f}x")
    print("Отчёт сохранён в REPORT.md")


if __name__ == "__main__":
    main()
