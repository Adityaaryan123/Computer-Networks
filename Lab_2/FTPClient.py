from ftplib import FTP

server_host = "ftp.dlptest.com"
username = "dlpuser"
access_key = "rNrKYTX9g7z3RgJRmxWuGHbeu"

try:
    with FTP(server_host, username, access_key) as ftp_client:
        print(f"Great! I'm now connected to the FTP server at {server_host}")
        
        ftp_client.set_pasv(False)

        upload_file_name = "upload_test.txt"
        with open(upload_file_name, "w") as test_file:
            test_file.write("Sample content for FTP upload testing.")
        
        with open(upload_file_name, "rb") as binary_file:
            ftp_client.storbinary(f"STOR {upload_file_name}", binary_file)
        print(f"\nAwesome! I just uploaded '{upload_file_name}' to the server")

        print("\nLet me show you what's on the server now:")
        ftp_client.dir()

        download_file_name = "downloaded_test.txt"
        with open(download_file_name, "wb") as local_file:
            ftp_client.retrbinary(f"RETR {upload_file_name}", local_file.write)
        print(f"\nPerfect! I downloaded the file and saved it as '{download_file_name}'")

except Exception as ftp_error:
    print(f"Oops! Something went wrong with the FTP operation: {ftp_error}")
