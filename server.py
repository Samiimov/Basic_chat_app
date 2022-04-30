import socket
from threading import Thread, Lock
import sys

def close_clients():
    """
    Close clients and parent thread.
    """
    # Closing clients
    for cs in client_sockets:
        client_sockets[cs]["socket"].close()
        # close server socket
    s.close()

def listen_for_client(cs, ca):
    """
    This function keep listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients
    """

    while True:
        try:
            # keep listening for a message from `cs` socket
            msg = cs.recv(1024).decode()
            print(msg +"1")
        except Exception:
            # client no longer connected
            # remove it from the set
            print(f"[!] Error: {ca} disconnected")
            del client_sockets[ca]
            sys.exit()
        else:
            # if we received a message, replace the <SEP> 
            # token with ": " for nice printing
            msg = msg.replace(separator_token, ": ")
            if "<NAME>" in msg:
                client_sockets[ca]["name"] = msg.split("<NAME> ")[-1]
                msg = msg.replace("<NAME>", "New user joined : ")

            for client_socket in client_sockets:
                client_sockets[client_socket]["socket"].send(msg.encode())

if __name__ == "__main__":
    # server's IP address
    SERVER_HOST = "localhost"
    SERVER_PORT = 5000 # port we want to use
    separator_token = "<SEP>" # we will use this to separate the client name & message

    # initialize list/set of all connected client's sockets
    client_sockets = {}
    # create a TCP socket
    s = socket.socket()
    # make the port as reusable port
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # bind the socket to the address we specified
    s.bind((SERVER_HOST, SERVER_PORT))
    # listen for upcoming connections
    s.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

    while True:
        # we keep listening for new connections all the time
        client_socket, client_address = s.accept()
        print(f"[+] {client_address} connected.")
        # add the new connected client to connected sockets
        client_sockets[client_address] = {}
        client_sockets[client_address]["socket"] = client_socket
        # start a new thread that listens for each client's messages
        t = Thread(target=listen_for_client, args=(client_socket, client_address))
        # make the thread daemon so it ends whenever the main thread ends
        t.daemon = True
        # start the thread
        t.start()