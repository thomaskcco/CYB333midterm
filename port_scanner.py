import socket
import time
from datetime import datetime


def scan_port(host: str, port: int, timeout: float = 0.5) -> bool:
    """
    Try to connect to a single TCP port.
    Returns True if open, False if closed or filtered.
    """

    # Create TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        result = sock.connect_ex((host, port))
        # connect_ex returns 0 if the connection succeeded
        return result == 0
    except socket.gaierror:
        # Hostname could not be resolved
        raise ValueError("Hostname could not be resolved.")
    except socket.timeout:
        # Treat timeout as closed/filtered
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error on port {port}: {e}")
        return False
    finally:
        sock.close()


def main():
    print("=== Simple Python Port Scanner ===")
    host = input("Enter host (e.g., 127.0.0.1 or scanme.nmap.org): ").strip()

    # Get port range input as strings first
    start_str = input("Enter start port (e.g., 20): ").strip()
    end_str = input("Enter end port (e.g., 1024): ").strip()

    # Validate port numbers
    try:
        start_port = int(start_str)
        end_port = int(end_str)
    except ValueError:
        print("[ERROR] Port values must be integers.")
        return

    # Check valid ranges
    if start_port < 1 or end_port > 65535 or start_port > end_port:
        print("[ERROR] Invalid port range. Ports must be 1-65535 and start <= end.")
        return

    print(f"\n[INFO] Starting scan on {host} from port {start_port} to {end_port}...")
    start_time = datetime.now()
    print(f"[INFO] Start time: {start_time}")

    try:
        for port in range(start_port, end_port + 1):
            # Small delay to be polite and avoid hammering the target
            time.sleep(0.05)

            try:
                is_open = scan_port(host, port)
            except ValueError as ve:
                print(f"[ERROR] {ve}")
                return

            if is_open:
                print(f"[OPEN ] Port {port}")
            else:
                # You can comment this out if it feels too noisy
                print(f"[CLOSED] Port {port}")
    except KeyboardInterrupt:
        print("\n[INFO] Scan interrupted by user.")
    finally:
        end_time = datetime.now()
        duration = end_time - start_time
        print(f"\n[INFO] Scan finished at: {end_time}")
        print(f"[INFO] Scan duration: {duration}")


if __name__ == "__main__":
    main()