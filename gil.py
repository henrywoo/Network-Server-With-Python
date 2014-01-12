'''
gil_detector.py

Detection of the gil is done by checking how fast multi-threaded code
is executed in relation to single-threaded code.
'''


import os
import threading
import timeit
import sys

ARBITRARY_COUNT_TO = 1024 * 100

  
def cpu_count_hack():
    if os.name.startswith('posix'):
        ncpus = os.sysconf('SC_NPROCESSORS_ONLN')
        if isinstance(ncpus, int) and ncpus > 0:
            return ncpus
    elif sys.platform.startswith('win'):
        ncpus = int(os.environ['NUMBER_OF_PROCESSORS']);
        if ncpus > 0:
            return ncpus
    elif sys.platform.startswith('java'):
        from java.lang import Runtime
        runtime = Runtime.getRuntime()
        ncpus = runtime.availableProcessors()
        if ncpus > 0:
            return ncpus
    if sys.platform.startswith('linux'):
        ncpus = int(os.popen2('grep -c processor /proc/cpuinfo')[1].read().strip())
        if ncpus > 0:
            return ncpus
    if sys.platform.startswith('darwin'):
        ncpus = int(os.popen2("sysctl -n hw.ncpu")[1].read())
        if ncpus > 0:
            return ncpus
    return 1 # Default

try:
    from multiprocessing import cpu_count
except ImportError:
    cpu_count = cpu_count_hack

class Worker(threading.Thread):
    def run(self):
        i = 0
        while i < ARBITRARY_COUNT_TO:
            i += 1
        
        return i

def start_workers(n):
    '''
    n workers are started that work on the given assignment.
    '''
    workers_list = [Worker() for i in range(n)]
    for worker in workers_list:
        worker.start()
    for worker in workers_list:
        worker.join()

def percentile_diff(a, b):
    return 2 * abs(b - a) / (b + a)

def count_python_cores():
    amount_of_work = 1
    best_effective_cpu_count = 0
    last_effective_cpu = 0
    while True:
        # the test
        times = timeit.Timer('start_workers(%d)' % amount_of_work, 'from __main__ import start_workers, Worker, ARBITRARY_COUNT_TO').repeat(repeat=5, number=5)
        
        time_to_finish = min(times)
        if amount_of_work == 1:
            baseline = time_to_finish

        effective_cpus = amount_of_work / (1.0 * time_to_finish / baseline)
        print('# of threads: %d, took %g, effectively %g cores' % (amount_of_work, time_to_finish, effective_cpus))
        
        if amount_of_work > 1:
            if effective_cpus > best_effective_cpu_count:
                best_effective_cpu_count = effective_cpus
            if percentile_diff(last_effective_cpu, effective_cpus) < 0.1:
                # a 20% shift isn't another core, it's an overhead quirk.
                return best_effective_cpu_count
            
        last_effective_cpu = effective_cpus
        amount_of_work += 1

def detect_gil():
    cores = cpu_count()
    effective = count_python_cores()
    print('Python is utilizing %.1f/%s cores' % (effective, cores))
    if effective / cores < 0.8:
        # ladies and gentleman, we have a GIL
        return True
    else:
        return False

if __name__ == "__main__":
    print(sys.version)
    if detect_gil():
        print('Sadly, you have a GIL.')
    else:
        print("Rejoice! You're awesome!")

