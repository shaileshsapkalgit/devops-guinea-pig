import subprocess
import json

NAMESPACE = "dev"
APP_NAME = "devops-guinea-pig"


def run_command(command):
    result = subprocess.run(
        command,
        shell=True,
        text=True,
        capture_output=True
    )

    return result.stdout.strip(), result.stderr.strip(), result.returncode


print("=" * 60)
print(" Kubernetes Troubleshooting")
print("=" * 60)

print(f"Application : {APP_NAME}")
print(f"Namespace   : {NAMESPACE}")


# --------------------------------------------------
# 1. GET PODS
# --------------------------------------------------

print("\n[1] Checking Pods...")

command = (
    f'kubectl get pods -n {NAMESPACE} '
    f'-l app.kubernetes.io/name={APP_NAME} '
    f'-o json'
)

stdout, stderr, returncode = run_command(command)

if returncode != 0:
    print("[ERROR] Failed to get Pods")
    print(stderr)
    exit(1)

pods = json.loads(stdout)

print(f"Found Pods: {len(pods['items'])}")


# --------------------------------------------------
# 2. ANALYZE EACH POD
# --------------------------------------------------

for pod in pods["items"]:

    pod_name = pod["metadata"]["name"]

    print("\n" + "-" * 60)
    print(f"Pod: {pod_name}")
    print("-" * 60)

    phase = pod["status"].get("phase")

    print(f"Status        : {phase}")

    containers = pod["status"].get("containerStatuses", [])

    for container in containers:

        container_name = container["name"]

        restart_count = container.get("restartCount", 0)

        ready = container.get("ready", False)

        print(f"Container     : {container_name}")
        print(f"Ready         : {ready}")
        print(f"Restart Count : {restart_count}")

        # Current state
        state = container.get("state", {})

        if "waiting" in state:

            reason = state["waiting"].get("reason", "Unknown")

            print(f"Current State : Waiting")
            print(f"Reason        : {reason}")

        elif "running" in state:

            print("Current State : Running")

        elif "terminated" in state:

            reason = state["terminated"].get("reason", "Unknown")
            exit_code = state["terminated"].get("exitCode")

            print("Current State : Terminated")
            print(f"Reason        : {reason}")
            print(f"Exit Code     : {exit_code}")

        # Last termination
        last_state = container.get("lastState", {})

        if "terminated" in last_state:

            terminated = last_state["terminated"]

            reason = terminated.get("reason", "Unknown")
            exit_code = terminated.get("exitCode")

            print("\nLast Termination")
            print(f"Reason        : {reason}")
            print(f"Exit Code     : {exit_code}")

            if reason == "OOMKilled":

                print(
                    "[WARNING] Container was killed due to memory exhaustion."
                )

            elif exit_code == 137:

                print(
                    "[WARNING] Exit code 137 detected. "
                    "Check for OOMKilled / SIGKILL."
                )

            elif exit_code != 0:

                print(
                    "[WARNING] Container exited with non-zero exit code."
                )


# --------------------------------------------------
# 3. POD EVENTS
# --------------------------------------------------

print("\n[2] Checking Pod Events...")

for pod in pods["items"]:

    pod_name = pod["metadata"]["name"]

    command = (
        f'kubectl describe pod {pod_name} '
        f'-n {NAMESPACE}'
    )

    stdout, stderr, returncode = run_command(command)

    if returncode == 0:

        print("\n" + "-" * 60)
        print(f"Events for: {pod_name}")
        print("-" * 60)

        # Print only Events section
        lines = stdout.splitlines()

        event_section = False

        for line in lines:

            if line.startswith("Events:"):
                event_section = True
                continue

            if event_section:
                print(line)

print("\n" + "=" * 60)
print(" Troubleshooting collection completed")
print("=" * 60)