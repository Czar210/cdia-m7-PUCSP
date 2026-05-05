import requests
import time
import sys

BASE = "http://127.0.0.1:8000"

def wait_for_server(timeout=20):
    for _ in range(timeout):
        try:
            r = requests.get(f"{BASE}/")
            if r.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.5)
    return False

def fail(msg):
    print("FAIL:", msg)
    sys.exit(1)

def main():
    print("Waiting for server...")
    if not wait_for_server():
        fail("Server did not start in time")

    print("Server up, running tests...")

    # Root
    r = requests.get(f"{BASE}/")
    if r.status_code != 200:
        fail(f"GET / returned {r.status_code}")

    # List pratos available
    r = requests.get(f"{BASE}/pratos", params={"disponivel": "true"})
    if r.status_code != 200:
        fail(f"GET /pratos returned {r.status_code}")

    # Validation: nome too short -> expect 422
    payload_bad = {"nome": "ab", "categoria": "pizza", "preco": 10}
    r = requests.post(f"{BASE}/pratos/input", json=payload_bad)
    if r.status_code == 201:
        fail("Invalid payload accepted (nome too short)")
    if r.status_code != 422:
        print("Note: expected 422 for invalid payload, got", r.status_code)
    else:
        body = r.json()
        for key in ("erro", "status", "path", "detalhes"):
            if key not in body:
                fail(f"Validation error response missing field: {key}")
        if not isinstance(body["detalhes"], list) or len(body["detalhes"]) == 0:
            fail("Validation error 'detalhes' should be a non-empty list")

    # Valid create
    payload = {"nome": "Teste Pizza", "categoria": "pizza", "preco": 33.5}
    r = requests.post(f"{BASE}/pratos/input", json=payload)
    if r.status_code != 201:
        fail(f"Creating prato failed: status {r.status_code}, body: {r.text}")
    created = r.json()
    if created.get("nome") != payload["nome"]:
        fail("Created prato mismatch")

    # Ensure it's listed
    r = requests.get(f"{BASE}/pratos")
    if r.status_code != 200:
        fail(f"GET /pratos after create failed: {r.status_code}")
    items = r.json()
    if not any(p.get("id") == created.get("id") for p in items):
        fail("Created prato not present in list")

    # 404 error format (non-existent resource)
    r = requests.get(f"{BASE}/pratos/99999")
    if r.status_code != 404:
        fail(f"Expected 404 for missing prato, got {r.status_code}")
    body = r.json()
    for key in ("erro", "status", "path", "detalhes"):
        if key not in body:
            fail(f"404 error response missing field: {key}")
    if body["status"] != 404:
        fail("404 response 'status' mismatch")

    # Business error format (invalid desconto)
    r = requests.post(f"{BASE}/pratos/1/aplicar_desconto", params={"percentual": 60})
    if r.status_code != 400:
        fail(f"Expected 400 for invalid desconto, got {r.status_code}")
    body = r.json()
    for key in ("erro", "status", "path", "detalhes"):
        if key not in body:
            fail(f"Business error response missing field: {key}")

    print("All tests passed")
    sys.exit(0)

if __name__ == '__main__':
    main()
