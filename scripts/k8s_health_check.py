import subprocess
import sys
import urllib.request
import urllib.error


# ==========================================
# Configuration
# ==========================================

NAMESPACE = "dev"
APP_NAME = "devops-guinea-pig-devops-guinea-pig"

HEALTH_URL = "https://localhost:8443/devops-guinea-pig/health"


# ==========================================
# Helper function
# ==========================================

def run_command(command):
    """Run a shell command and return its output."""

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )

        return result.stdout.strip()

    except subprocess.CalledProcessError as error:
        print(f"[ERROR] Command failed: {' '.join(command)}")
        print(error.stderr.strip())
        return None


# ==========================================
# 1. Check Pods
# ==========================================

def check_pods():

    print("\n[1] Checking Pods...")

    output = run_command([
        "kubectl",
        "get",
        "pods",
        "-n",
        NAMESPACE,
        "-l",
        f"app.kubernetes.io/name=devops-guinea-pig",
        "--no-headers"
    ])

    if not output:
        print("[FAIL] No application pods found")
        return False

    lines = output.splitlines()

    ready_pods = 0

    for line in lines:

        columns = line.split()

        if len(columns) >= 2:

            ready = columns[1]

            if ready.startswith("1/1"):
                ready_pods += 1

    print(f"Found Pods: {len(lines)}")
    print(f"Ready Pods: {ready_pods}")

    if ready_pods == len(lines):
        print("[PASS] All application Pods are Ready")
        return True

    print("[FAIL] Some application Pods are not Ready")
    return False


# ==========================================
# 2. Check Service
# ==========================================

def check_service():

    print("\n[2] Checking Service...")

    output = run_command([
        "kubectl",
        "get",
        "service",
        APP_NAME,
        "-n",
        NAMESPACE,
        "--no-headers"
    ])

    if output:
        print("[PASS] Service exists")
        print(output)
        return True

    print("[FAIL] Service not found")
    return False


# ==========================================
# 3. Check Endpoints
# ==========================================

def check_endpoints():

    print("\n[3] Checking Endpoints...")

    output = run_command([
        "kubectl",
        "get",
        "endpoints",
        APP_NAME,
        "-n",
        NAMESPACE,
        "-o",
        "jsonpath={.subsets[*].addresses[*].ip}"
    ])

    if output:
        endpoints = output.split()

        print(f"Endpoints found: {len(endpoints)}")
        print(f"IPs: {output}")

        print("[PASS] Service has backend endpoints")
        return True

    print("[FAIL] No backend endpoints found")
    return False


# ==========================================
# 4. Check HTTP Health
# ==========================================

def check_http_health():

    print("\n[4] Checking Application Health Endpoint...")

    try:

        # Local environment uses self-signed certificate
        import ssl

        ssl_context = ssl._create_unverified_context()

        response = urllib.request.urlopen(
            HEALTH_URL,
            context=ssl_context,
            timeout=10
        )

        status_code = response.status
        body = response.read().decode()

        print(f"HTTP Status: {status_code}")
        print(f"Response: {body}")

        if status_code == 200:

            print("[PASS] Application health check successful")
            return True

        print("[FAIL] Application returned non-200 status")
        return False

    except urllib.error.URLError as error:

        print(f"[FAIL] Health endpoint unavailable: {error}")
        return False

    except Exception as error:

        print(f"[FAIL] Unexpected error: {error}")
        return False


# ==========================================
# Main
# ==========================================

def main():

    print("=" * 50)
    print(" Kubernetes Application Health Check")
    print("=" * 50)

    print(f"Application : {APP_NAME}")
    print(f"Namespace   : {NAMESPACE}")

    pod_status = check_pods()

    service_status = check_service()

    endpoint_status = check_endpoints()

    http_status = check_http_health()

    print("\n" + "=" * 50)
    print(" FINAL RESULT")
    print("=" * 50)

    if (
        pod_status
        and service_status
        and endpoint_status
        and http_status
    ):

        print("Overall Status : HEALTHY")

        sys.exit(0)

    else:

        print("Overall Status : UNHEALTHY")

        sys.exit(1)


if __name__ == "__main__":
    main()