from Socket import Socket
import asyncio

class Server(Socket):
    def __init__(self):
        super(Server, self).__init__()
        self.users = [] # масив користувачів

    def set_up(self):
        self.socket.bind(("127.0.0.1", 1234))
        self.socket.listen(4)
        self.socket.setblocking(False)
        print("Server is listening")

    # відправляємо дані користувачам
    async def send_data(self, data=None):
        for user in self.users:
            await self.main_loop.sock_sendall(user, data)

    # слухаємо користувача(-ів)
    async def listen_socket(self, listened_socket=None):
        #print("Listening user")
        if not listened_socket:
            return

        while True:
            data = self.main_loop.sock_recv(listened_socket, 2048)
            print(f"User sent {data}")

            await self.send_data(data)

    # запуск сервера
    async def accept_sockets(self):
        while True:
            user_socket, address = await self.main_loop.sock_accept(self.socket)
            print(f"User <{address[0]}> connected") # 
        
            # додаємо користувачів у масив
            self.users.append(user_socket)
            self.main_loop.create_task(self.listen_socket(user_socket))

    
    async def main(self):
        await self.main_loop.create_task(self.accept_sockets())                         


    
if __name__ == '__main__':
    server = Server()
    server.set_up()

    server.start()
