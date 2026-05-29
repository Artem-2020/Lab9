import json
import subprocess
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
GO_PROGRAM = ROOT_DIR / "go_json_worker" / "main.go"


def send_request_to_go(payload):
    process = subprocess.run(
        ["go", "run", str(GO_PROGRAM)],
        input=json.dumps(payload, ensure_ascii=False),
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(process.stdout)


def main():
    payload = {
        "user": "Вариант 9",
        "operation": "average",
        "numbers": [3, 5, 7, 8, 9],
    }

    response = send_request_to_go(payload)
    print(json.dumps(response, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

