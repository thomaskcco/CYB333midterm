import socket

HOST = "127.0.0.1"  # Loopback (your own machine)
PORT = 5000         # Any free port above 1024 is usually fine


def start_server():
    """Start a simple TCP server that accepts one client and echoes messages."""

    # Create TCP socket (IPv4, TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow quick restart if you stop/restart the script
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # Bind to address and port
        server_socket.bind((HOST, PORT))
        print(f"[SERVER] Bound to {HOST}:{PORT}")

        # Start listening for incoming connections
        server_socket.listen()
        print("[SERVER] Listening for connections...")

        # Accept a single client connection
        conn, addr = server_socket.accept()
        print(f"[SERVER] Connected by {addr}")

        # Use context manager so the connection closes cleanly
        with conn:
            while True:
                # Receive up to 1024 bytes
                data = conn.recv(1024)

                # If no data, client closed the connection
                if not data:
                    print("[SERVER] Client disconnected.")
                    break

                # Decode bytes to string
                message = data.decode("utf-8")
                print(f"[SERVER] Received: {message}")

                # Build a response
                response = f"Server received: {message}"

                # Send response back to client
                conn.sendall(response.encode("utf-8"))
                print(f"[SERVER] Sent: {response}")

    except KeyboardInterrupt:
        print("\n[SERVER] Interrupted by user. Shutting down.")
    except Exception as e:
        print(f"[SERVER] Error: {e}")
    finally:
        # Always close the listening socket
        server_socket.close()
        print("[SERVER] Socket closed.")


if __name__ == "__main__":
    start_server()
