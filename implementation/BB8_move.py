# import threading
from implementation.BB8_driver import *

# class Move(threading.Thread):
#     def __init__(self, client, rho, phi):
#         threading.Thread.__init__(self)
#         self.client = client
#         self.rho = rho
#         self.phi = phi
        
#     def run(self):
#         self.client.roll(self.rho, self.phi, 0o1, True)

class Move:
    def __init__(self, client):
        self.client = client
        
    def drive(self, rho, phi, runtime):
        self.client.roll(rho, phi, 0o1, True)
        time.sleep(runtime)
        # self.client.roll(0, phi, 0o1, True)
        # time.sleep(runtime)