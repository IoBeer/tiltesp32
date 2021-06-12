import gc
try:
  import usocket as socket
except:
  import socket

def web_page():
  html = """<!DOCTYPE HTML><html><head><title>Hello TiltESP32</title></head><body>Hello TitlESP32</body></html>"""
  return html

def start_webserver():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
 
    while True:
        try:
            if gc.mem_free() < 102000:
                gc.collect()
            conn, addr = s.accept()
            conn.settimeout(3.0)
            print('Got a connection from %s' % str(addr))
            request = conn.recv(1024)
            conn.settimeout(None)
            request = str(request)
            response = web_page()
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
            conn.close()
        except OSError as e:
            conn.close()
            print('Connection closed')
