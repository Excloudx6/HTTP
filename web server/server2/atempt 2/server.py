import socket

class server():
    def __init__(self):
        self.host_ip = socket.gethostbyname(socket.gethostname())
        self.host_port = 81
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_recv_size = 1024

    def get_data(self, conn):
        """ gets the data from client """
        data = b""
        while b"\r\n\r\n" not in data:
            data += conn.recv(self.data_recv_size)
        return data

    def server(self):
        """ main method starts the server """
        print(f"[+] Server started listening on port {self.host_port}!")
        print(f"[+] Server Ip: {self.host_ip}")
        self.s.bind((self.host_ip, self.host_port))
        self.s.listen()

        while True:
            conn, addr = self.s.accept()
            with conn:
                data = self.get_data(conn)
                
                # GET request
                if data[0:5] == b"GET /":
                    index = open("index.html", "rb").read()
                    conn.sendall(b"HTTP/1.0 200 OK\nContent-Type: text/html\n\n" + index)
                    print("[+] Responded to GET request")

                # POST request
                elif data[0:4] == b"POST":
                    with open("output.txt", "ab") as file:
                        file.write(data)
                        print(f"{len(data)} bytes received from post!")
                        conn.sendall(b"HTTP/1.0 200 OK\r\nContent-Type: text/html")

s = server()
s.server()
