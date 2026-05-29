import ctypes
import subprocess
import sys
import time
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
RUST_SOURCE = ROOT_DIR / "rust" / "speed.rs"
BUILD_DIR = ROOT_DIR / "build"


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
        [
            "rustc",
            "--crate-type",
            "cdylib",
            "-O",
            str(RUST_SOURCE),
            "-o",
            str(output),
        ],
        check=True,
    )
    return output


def python_count_primes(limit):
    count = 0
    for number in range(2, limit + 1):
        if is_prime(number):
            count += 1
    return count


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


def measure(function, *args, repeats=5):
    best_time = float("inf")
    result = None

    for _ in range(repeats):
        started_at = time.perf_counter()
        result = function(*args)
        elapsed = time.perf_counter() - started_at
        best_time = min(best_time, elapsed)

    return result, best_time


def main():
    limit = 100_000
    rust_library = ctypes.CDLL(str(compile_rust_library()))
    rust_count_primes = rust_library.rust_count_primes
    rust_count_primes.argtypes = [ctypes.c_uint32]
    rust_count_primes.restype = ctypes.c_uint32

    python_result, python_time = measure(python_count_primes, limit)
    rust_result, rust_time = measure(rust_count_primes, limit)

    if python_result != rust_result:
        raise RuntimeError(
            f"Результаты не совпали: Python={python_result}, Rust={rust_result}"
        )

    print(f"Функция: подсчет простых чисел от 2 до {limit}")
    print(f"Результат: {python_result}")
    print(f"Python: {python_time:.6f} сек.")
    print(f"Rust:   {rust_time:.6f} сек.")
    print(f"Rust быстрее примерно в {python_time / rust_time:.1f} раз")


if __name__ == "__main__":
    main()

