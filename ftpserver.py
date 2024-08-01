# Adapted from co pilot
import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# Define FTP server settings
FTP_HOST = "10.112.4.114"  # Change to your desired host
FTP_PORT = 21
FTP_USER = "adminr"  # Change to your desired username
FTP_PASSWORD = "passer"  # Change to your desired password
FTP_DIRECTORY = r"G:\Co-Op Students\CO-Op Projects Summer Term 2024\Joseph Bagheri\joecode\GPS"  # Change to your desired directory

# Create an authorizer with a dummy user
authorizer = DummyAuthorizer()
authorizer.add_user(FTP_USER, FTP_PASSWORD, FTP_DIRECTORY, perm="elradfmw")

# Create an FTP handler
handler = FTPHandler
handler.authorizer = authorizer 

# Create the FTP server
server = FTPServer((FTP_HOST, FTP_PORT), handler)

# Start the server
PID = os.getpid()
print(f"Starting FTP server on {FTP_HOST}:{FTP_PORT}...")
server.serve_forever()

# To stop use comand:
# kill <PID>

# To find the <PID> of the server:
# netstat -ano | findstr FTP_HOST:FTP_PORT

# Example:
# netstat -ano | findstr 10.112.4.114:21
# The <PID> number will be the last column

# Where <PID> is the process id (may be visible in the terminal after executing the code).