import psutil

CPU_LIMIT = 80
MEM_LIMIT = 80

def can_run():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    return cpu < CPU_LIMIT and mem < MEM_LIMIT
