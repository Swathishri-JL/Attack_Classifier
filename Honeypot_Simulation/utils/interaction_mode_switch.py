def switch_to_high_interaction(conn):
    print("Switching to high-interaction mode...")
    
    # Log the escalation
    with open('logs/honeypot_log.txt', 'a') as f:
        f.write("High-interaction mode triggered.\n")
    
    # Engage the attacker with a more realistic session
    conn.sendall(b"Welcome to the high-interaction honeypot!\n")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"Received: {data.decode()}")
        conn.sendall(b"Command received.\n")
    conn.close()
