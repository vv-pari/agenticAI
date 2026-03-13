import subprocess, sys

def main():
    cmd = [sys.executable, "run.py", "--mode", "mock", "--data", "data/tickets_sample.json", "--limit", "1"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        print("SMOKE TEST FAILED")
        print(p.stdout)
        print(p.stderr)
        raise SystemExit(1)
    print("SMOKE TEST PASSED")
    print(p.stdout.splitlines()[-8:])

if __name__ == "__main__":
    main()
