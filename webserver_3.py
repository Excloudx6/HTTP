import socket, re, time, os, threading

class Server():
    def __init__(self):
        self.host_ip = socket.gethostbyname(socket.gethostname())
        self.host_port = 81
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.data_recv_size = 16384
        self.ok_200 = b"HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n"
        self.max_size = 100_000_000

    def print_percent(self, size):
        ''' Purely for visual purposes, shows a percent complete while downloading the file'''
        if size > -1:
            print("[+] Downloading file!")
            start = time.time()
            self.byte_count = len(self.data)
            percent = ((self.byte_count / int(size))*100)
            while percent < 100:
                self.byte_count = len(self.data)
                percent = ((self.byte_count / int(size))*100)
                print(f"[+] Downloading file {percent}% complete!")
                time.sleep(2)
            print(f"[+] Total download time {round(time.time() - start, 2)} seconds")

    def get_data(self, conn, size=-1, do_print=True):
        ''' Fetches the file from client, call this method when respoding to POST'''
        self.data = b""
        self.byte_count = 0
        if do_print == True:
            show_percent = threading.Thread(target=self.print_percent, args=[size])
            show_percent.start()

        # process packet header (loop until recived data is less then 16384)
        if size == -1:
            chunk = conn.recv(self.data_recv_size)
            while len(chunk) >= self.data_recv_size:
                chunk = conn.recv(self.data_recv_size)
                self.data += chunk
                
            return self.data + chunk

        # process packet body (loop for length of body)
        # to make this loop as fast as possible, it should only contain conn.recv
        for i in range(0, size, self.data_recv_size):
            self.data += conn.recv(self.data_recv_size)
            
        return self.data
                
    def save_file(self, body):
        print("[+] extracting file data!")
        name = re.compile(b'name="uploadedfile"; filename="(.+)"').search(body).group(1)
        data = re.compile(b"WebKitFormBoundary((\n|.)*)Content-Type.+\n.+?\n((\n|.)*)([\-]+WebKitFormBoundary)?")
        print("[+] Saving file to disk!")
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
                    print([length])

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

# to do list:
# inside of get_data
# packet processing loop could use multi-threading to download multiple chunks at once
# this may make it faster

# ram:
# memory managment needs to be inplace for very large files
# files too large to fit completly in RAM.

# re:
# the save file regular expression is taking way to long
# don't use expressions in save_file
