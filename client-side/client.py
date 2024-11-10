from socket import *
import threading

def client_thread (client_socket: socket):
	closeConnectionStr = "Conexão fechada!"

	try:
		while True:
				option = input ("Selecione uma opção\n1 - Enviar um arquivo | 2 - Receber o último arquivo armazenado no servidor: ")
				client_socket.send(option.encode())
				
				response = client_socket.recv(1024)
				print ("(SERVER):", response.decode())

				if (response.decode() == closeConnectionStr):
					break

				if (option == "1"):
					filename = "file.txt"
					print (f"Enviando arquivo {filename} para o servidor...")
					
					client_socket.send(filename.encode())
					response = client_socket.recv(1024)
					print ("(SERVER):", response.decode())
					
					with (open (filename, "rb") as file):
						while (chunk := file.read(1024)):
							client_socket.send(chunk)
							print (f"Enviado {len(chunk)} bytes")
					
					client_socket.send(b"<END>")
					print ("Arquivo enviado com sucesso.")

				elif (option == "2"):
					with (open ("received_file.txt", "wb") as file):
						while True:
							data = client_socket.recv(1024)

							if (data == b"<END>"):
								break

							file.write (data)
					
					print ("Arquivo recebido com sucesso.")

				response = client_socket.recv(1024).decode()
				print ("Do servidor:", response)
	
	except Exception as e:
		print(f"Error: {e}")
	
	finally:
		client_socket.close()
		print ("Conexão com o servidor fechada.")

def run_client ():
	server_ip = "127.0.0.1"
	serverPort = 22000

	try:
		clientSocket = socket (AF_INET, SOCK_STREAM)
		socket.connect (clientSocket, (server_ip, serverPort))

		client_thread (client_socket=clientSocket)
	
	except Exception as e:
		print(f"Error: {e}")

run_client()