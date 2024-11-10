from socket import *
import threading

def handle_client (clientConnectionSocket: socket, adress: tuple[str, int]):

	connectionCloseStr = "q"

	try:
		while True:
			option = clientConnectionSocket.recv(1).decode()

			if (option.lower() == connectionCloseStr):
				clientConnectionSocket.send("Conexão fechada!".encode())
				break

			clientConnectionSocket.send("OK.".encode())

			print(f"Received: {option}")

			if (option == "1"): # receber arquivo do cliente
				filename = clientConnectionSocket.recv(16).decode()
				print(f"Salvando arquivo recebido como {filename}")
				clientConnectionSocket.send(f"Arquivo {filename} sendo gravado.".encode())
				
				with open(filename, "wb") as file:
					while True:
						data = clientConnectionSocket.recv(1024)
						
						if data == b"<END>":
							break
						
						print (f"Recebido {len(data)} bytes.")
						file.write (data)
				
				print ("Arquivo recebido e armazenado com sucesso.")
				clientConnectionSocket.send("Arquivo recebido e armazenado!".encode())

			elif (option == "2"): # enviar ultimo arquivo para cliente
				filename = "file.txt"
				
				with open (filename, "rb") as file:
					while (chunk := file.read (1024)):
						clientConnectionSocket.send(chunk)
				
				clientConnectionSocket.send (b"<END>")
				clientConnectionSocket.send ("Arquivo enviado.".encode())	
		
	except Exception as e:
		print(f"Error handling client: {e}")
		
	finally:
		clientConnectionSocket.close()
		print(f"Conexão com cliente de endereço {adress[0]}:{adress[1]} fechada.")
		

def run_server ():
	server_ip = "127.0.0.1"
	serverPort = 22000
	
	try:
		serverSocket = socket (AF_INET, SOCK_STREAM) # socket de escuta
		serverSocket.bind ((server_ip, serverPort))

		serverSocket.listen()
		print(f"Escutando no endereço {server_ip}:{serverPort}")

		while True:
			clientConnectionSocket, clientAdress = serverSocket.accept()
			print(f"Conexão aceita do endereço {clientAdress[0]}:{clientAdress[1]}") # accept cria um novo socket para se comunicar com o cliente

			client_thread = threading.Thread(target=handle_client, args=(clientConnectionSocket, clientAdress))
			client_thread.start()

	except Exception as e:
		print (f"Error: {e}")
	
	finally:
		serverSocket.close()

run_server ()