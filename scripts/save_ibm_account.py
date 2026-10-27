"""Save an IBM Quantum API key from a downloaded IBM Cloud key file into the user's Qiskit profile.

Usage (from the sentinel_sim folder):
    .venv\\Scripts\\python.exe scripts\\save_ibm_account.py apikey.json

The key is written by qiskit-ibm-runtime to ~/.qiskit/qiskit-ibm.json, outside the repository. The value is never
printed. After saving, the script lists the devices visible to the account, which costs no QPU time. Delete the
downloaded key file once this succeeds.
"""
import json
import sys
from pathlib import Path

from qiskit_ibm_runtime import QiskitRuntimeService


def main() -> None:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "apikey.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    token = data.get("apikey") or data.get("apiKey") or data.get("token")
    if not token:
        sys.exit(f"no 'apikey' field found in {path}")
    QiskitRuntimeService.save_account(channel="ibm_quantum_platform", token=token, overwrite=True)
    print("account saved to ~/.qiskit/qiskit-ibm.json")
    service = QiskitRuntimeService()
    names = [b.name for b in service.backends()]
    print("devices visible to this account:", names)
    print("you can now delete", path)


if __name__ == "__main__":
    main()
