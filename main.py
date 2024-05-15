import RPi.GPIO as GPIO
import time
import socket

TRIG = 21
ECHO = 20

GPIO.setmode(GPIO.BCM)

def calculate_distance():
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    
    GPIO.output(TRIG, False)
    time.sleep(0.2)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = time.time()
    pulse_end = time.time()

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

def send_data(client_socket):
    try:
        while True:
            for angle in range(15, 166):
                distance = calculate_distance()
                data = str(angle) + "," + str(distance) + "."
                print(data, end="", flush=True)
                client_socket.send(data.encode())
                time.sleep(0.1)
            
            for angle in range(165, 14, -1):
                distance = calculate_distance()
                data = str(angle) + "," + str(distance) + "."
                print(data, end="", flush=True)
                client_socket.send(data.encode())
                time.sleep(0.1)

    except (ConnectionResetError, BrokenPipeError):
        print("Connection reset. Waiting for new connection...")

def main():
    # Set up socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8888))  # Change the port if needed
    server_socket.listen(1)
    print("Waiting for connection...")
    
    while True:
        client_socket, client_address = server_socket.accept()
        print("Connection from:", client_address)
        
        send_data(client_socket)

    server_socket.close()

if __name__ == "__main__":
    main()
