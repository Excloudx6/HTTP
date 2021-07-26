import socket, re, time, os

class Server():
    def __init__(self):
        self.host_ip = socket.gethostbyname(socket.gethostname())
        self.host_port = 81
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.data_recv_size = 1024
        self.ok_200 = b"HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n"
        self.max_size = 100_000_000

    def get_data(self, conn, size=-1):
        data = b""
        byte_count = 0
        prev_time = time.time() + 1
        while True:
            chunk = conn.recv(self.data_recv_size)
            byte_count += self.data_recv_size

            if time.time() >= prev_time:
                prev_time = time.time() + 1
                percent = ((byte_count / int(size))*100)
                print(f"[+] Downloading file {percent}% complete!")
                
            if size == -1 and len(chunk) < self.data_recv_size:
                return data + chunk
            
            elif byte_count >= size:
                return data + chunk
            else:
                data += chunk
                
    def save_file(self, body):
        name = re.compile(b'name="uploadedfile"; filename="(.+)"').search(body).group(1)
        data = re.compile(b"WebKitFormBoundary((\n|.)*)Content-Type.+\n.+?\n((\n|.)*)([\-]+WebKitFormBoundary)?")
        with open(name, "wb") as file:
            file.write(data.search(body).group(3))
        os.popen("python zcreate_index_post.py")
        self.form = self.form = open("index.html", "rb").read()

    def run(self):
        print(f"[+] Server: http://{self.host_ip}:{self.host_port}")
        self.s.bind((self.host_ip, self.host_port))
        self.s.listen()

        while True:
            try:
                self.form = self.form = open("index.html", "rb").read()
                conn,addr = self.s.accept()
                header = self.get_data(conn)

                # GET request
                if header[0:5] == b"GET /":
                    conn.sendall(b"HTTP/1.0 200 OK\nContent-Type: text/html\n\n"+self.form)
                    print("[+] Responded to GET request!")

                # POST request
                elif header[0:4] == b"POST":
                    length = int(header.split(b"Content-Length: ")[1].split(b"\n")[0].decode("ASCII"))

                    # check for large file
                    if length >= self.max_size:
                        print(f"File to Large! {length / 1024 / 1024}MB, max file size {self.max_size/1024/1024}MB!")
                        conn.sendall(b"HTTP/1.0 403 Forbidden\r\n\r\nFailed to upload File to large, max size %d!" % self.max_size)
                        conn.close()

                    # download file
                    body = self.get_data(conn, length)
                    self.save_file(body)

                    # send OK reponse to server
                    conn.sendall(self.ok_200+b"Successfully upload %d bytes to the server!" % len(body))
                    self.form = self.form = open("index.html", "rb").read()
                    print(f"[+] {len(body)} bytes received from POST!")

            except FileNotFoundError:
                with open("index.html", "w") as file:
                    file.write("""<form enctype="multipart/form-data" action="" method="POST">
                                    <input type="hidden" name="MAX_FILE_SIZE" value="8000000" />
                                    <input name="uploadedfile" type="file" /><br />
                                    <input type="submit" value="Upload File" />
                                </form>""")
                
            except Exception as error:
                print(error)
                conn.close()


s = Server()
s.run()
