import socket

HOST = "127.0.0.1"  # Same as server
PORT = 5000         # Same as server


def run_client():
    """Connect to the server and send messages typed by the user."""

    # Create TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Try to connect to server
        sock.connect((HOST, PORT))
        print(f"[CLIENT] Connected to {HOST}:{PORT}")
    except ConnectionRefusedError:
        # This happens if server is not running
        print("[CLIENT] Connection refused. Is the server running?")
        return
    except Exception as e:
        print(f"[CLIENT] Connection error: {e}")
        return

    try:
        while True:
            message = input("Enter message (or 'quit' to exit): ")

            if message.lower() == "quit":
                print("[CLIENT] Closing connection and exiting.")
                break

            # Send message to server
            sock.sendall(message.encode("utf-8"))

            # Wait for server response
            data = sock.recv(1024)

            # If no data, server closed connection
            if not data:
                print("[CLIENT] Server closed the connection.")
                break

            print(f"[CLIENT] Received: {data.decode('utf-8')}")

    except KeyboardInterrupt:
        print("\n[CLIENT] Interrupted by user.")
    except Exception as e:
        print(f"[CLIENT] Error during send/receive: {e}")
    finally:
        # Close socket
        sock.close()
        print("[CLIENT] Socket closed.")


if __name__ == "__main__":
    run_client()
