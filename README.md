Орехов Артем Алексеевич, группа 221331, Лабораторная работа 9, вариант 9, сложность средняя
# Лабораторная работа №9, вариант 9

Выполнены задания средней сложности:

1. Передача данных из Python в Go через JSON (`stdin`/`stdout`).
2. Добавление горутины для фоновой обработки запросов.
3. Сравнение скорости Rust-функции и аналогичной функции на Python.

## Структура

- `python_to_go.py` - Python-скрипт, который передает JSON в Go-программу.
- `go_json_worker/main.go` - Go-программа, которая читает JSON из `stdin`, обрабатывает запрос в горутине и возвращает JSON в `stdout`.
- `rust/speed.rs` - Rust-функция `rust_count_primes`.
- `benchmark_rust_vs_python.py` - Python-бенчмарк, который компилирует Rust в динамическую библиотеку и сравнивает ее с Python-функцией.

## Запуск задания 4 и 2

```powershell
python .\python_to_go.py
```

Пример результата:

```json
{
  "message": "Данные успешно обработаны в Go",
  "operation": "average",
  "result": 6.4,
  "processed_by": "background goroutine"
}
```

## Запуск задания 9

```powershell
python .\benchmark_rust_vs_python.py
```

Скрипт сам компилирует `rust/speed.rs` в папку `build` и затем выводит время выполнения Python- и Rust-варианта функции подсчета простых чисел.

