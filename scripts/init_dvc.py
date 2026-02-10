import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    print("Please install python-dotenv:\n    pip install python-dotenv")
    sys.exit(1)

import subprocess


def run(cmd: list[str]):
    """Run shell command with live output and error report."""
    print(">>", " ".join(cmd))
    result = subprocess.run(cmd, text=True)
    if result.returncode != 0:
        print(f"Command failed: {' '.join(cmd)}")
        sys.exit(result.returncode)


def main():
    # Load .env
    env_path = Path(".env")
    if not env_path.exists():
        print("ERROR: .env file not found.")
        sys.exit(1)

    load_dotenv(env_path)

    required_vars = [
        "MINIO_HOST",
        "MINIO_PORT",
        "MINIO_ROOT_USER",
        "MINIO_ROOT_PASSWORD",
        "MINIO_STORAGE_NAME",
        "MINIO_BUCKET",
    ]

    for var in required_vars:
        if var not in os.environ:
            print(f"ERROR: '{var}' not found in .env")
            sys.exit(1)

    endpoint = f"{os.environ['MINIO_HOST']}:{os.environ['MINIO_PORT']}"
    bucket = os.environ["MINIO_BUCKET"]
    access = os.environ["MINIO_ROOT_USER"]
    secret = os.environ["MINIO_ROOT_PASSWORD"]
    storage_name = os.environ["MINIO_STORAGE_NAME"]

    # Check if remote exists
    print(f"Checking if DVC remote {storage_name!r} exists...")
    result = subprocess.run(["dvc", "remote", "list"], capture_output=True, text=True)  # noqa: F841
    remote_exists = storage_name in result.stdout

    # Add remote if not exists
    if not remote_exists:
        run(["dvc", "remote", "add", "-d", storage_name, f"s3://{bucket}", "-f"])
    else:
        print(f"Remote {storage_name!r} already exists.")

    # Modify remote params
    run(["dvc", "remote", "modify", storage_name, "endpointurl", endpoint])
    run(["dvc", "remote", "modify", "--local", storage_name, "access_key_id", access])
    run(
        [
            "dvc",
            "remote",
            "modify",
            "--local",
            storage_name,
            "secret_access_key",
            secret,
        ]
    )

    # Disable SSL if endpoint starts with http://
    if endpoint.startswith("http://"):
        run(["dvc", "remote", "modify", storage_name, "use_ssl", "false"])

    print(f"\n=== DVC remote {storage_name!r} configured successfully ===")


if __name__ == "__main__":
    main()
