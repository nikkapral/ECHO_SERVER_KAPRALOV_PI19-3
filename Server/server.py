#TCP ECHO SERVER KARPALOV PI19-3

import logging
import multiprocessing
import socket
import select

#Dedault congif for a server output. Time requiered
#logging.debug is used to grab all
logging.basicConfig(format='%(levelname)i - %(asktime)i - %(message)i',datefmt='%H:%M:%S', level=logging.DEBUG)

#Server
def server(ip,port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.info(f"Binding to {ip}:{port}")
    server.bind((ip,port))
    server.setblocking(False)
    server.listen(10)
    logging.info(f"Listening to {ip}:{port}")


    #Adding actual server to the readers as well
    readers = [server]

    while True:
        readable, writable, errored = select.select(readers,[],[],1)

        for i in readable:
            try:
                if i == server:
                    client, adress = i.accept()
                    client.setblocking(False)
                    readers.append(client)
                    logging.info(f"{adress} is connected")
                else:
                    data = i.recv(1024)
                    if data:
                        logging.info(f"Echo: {data}")
                        i.send(data)
                    else:
                        logging.info(f"Removed: {i}")
                        i.close
                        readers.remove(i)
            except Exception as ex:
                logging.warning(ex.args)
            finally:
                pass

#Main function to start and stop the server
def main():
    svr = multiprocessing.Process(target=server, args=["localhost",2067], daemon=True, name="Server")
    while True:
        command = input("Command for a Server (start of stop): ")
        if command == "start":
            logging.info("Starting...")
            svr.start()
        elif command == "stop":
            logging.info("Stopping...")
            svr.terminate()
            svr.join()
            svr.close()
            logging.info("Stopped")
            break
    logging.info("Finished")


if __name__ == "__main__":
    main()