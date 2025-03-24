import random

class Track():
    def __init__(self, instruments):
        self.instruments = []
    
    def add(self, instrument):
        self.instruments.append(instrument)