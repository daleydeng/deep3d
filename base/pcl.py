from . import signal

def save_pc(pc, fname):
    pc.to_file(fname.encode())
