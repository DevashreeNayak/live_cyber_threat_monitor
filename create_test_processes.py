"""
Create test processes to simulate normal and suspicious behavior
Run this script to generate processes for your cyber threat monitor to detect
"""

import multiprocessing
import time
import random
import hashlib
import os
from datetime import datetime

def normal_process(process_id, duration=60):
    """Simulates a normal process with low CPU/memory usage"""
    print(f"[NORMAL-{process_id}] Started at {datetime.now().strftime('%H:%M:%S')}")
    
    start_time = time.time()
    data = []
    
    while time.time() - start_time < duration:
        # Light computation - normal behavior
        for i in range(1000):
            data.append(i * 2)
        
        # Small memory usage
        if len(data) > 10000:
            data = data[-5000:]
        
        time.sleep(0.5)  # Sleep to keep CPU low
    
    print(f"[NORMAL-{process_id}] Finished")

def cpu_intensive_process(process_id, duration=60):
    """Simulates a suspicious process with HIGH CPU usage"""
    print(f"[SUSPICIOUS-CPU-{process_id}] ⚠️  Started at {datetime.now().strftime('%H:%M:%S')}")
    
    start_time = time.time()
    
    while time.time() - start_time < duration:
        # Heavy computation - suspicious behavior
        result = 0
        for i in range(1000000):
            result += i ** 2
            hashlib.sha256(str(result).encode()).hexdigest()
        
        # No sleep = high CPU usage
    
    print(f"[SUSPICIOUS-CPU-{process_id}] Finished")

def memory_intensive_process(process_id, duration=60):
    """Simulates a suspicious process with HIGH memory usage"""
    print(f"[SUSPICIOUS-MEM-{process_id}] ⚠️  Started at {datetime.now().strftime('%H:%M:%S')}")
    
    start_time = time.time()
    large_data = []
    
    while time.time() - start_time < duration:
        # Allocate lots of memory - suspicious behavior
        large_data.append([random.random() for _ in range(100000)])
        
        time.sleep(2)
    
    print(f"[SUSPICIOUS-MEM-{process_id}] Finished")

def network_simulator_process(process_id, duration=60):
    """Simulates a process with network-like behavior (CPU spikes)"""
    print(f"[SUSPICIOUS-NET-{process_id}] ⚠️  Started at {datetime.now().strftime('%H:%M:%S')}")
    
    start_time = time.time()
    
    while time.time() - start_time < duration:
        # Simulate network packet processing
        packets = []
        for _ in range(50000):
            packet = hashlib.md5(os.urandom(64)).hexdigest()
            packets.append(packet)
        
        time.sleep(1)
    
    print(f"[SUSPICIOUS-NET-{process_id}] Finished")

def file_access_simulator(process_id, duration=60):
    """Simulates high file access activity"""
    print(f"[SUSPICIOUS-FILE-{process_id}] ⚠️  Started at {datetime.now().strftime('%H:%M:%S')}")
    
    start_time = time.time()
    temp_files = []
    
    try:
        while time.time() - start_time < duration:
            # Create and delete temporary files
            filename = f"temp_test_{process_id}_{time.time()}.txt"
            with open(filename, 'w') as f:
                f.write("test data" * 1000)
            temp_files.append(filename)
            
            # Read the file
            with open(filename, 'r') as f:
                _ = f.read()
            
            time.sleep(0.1)
    finally:
        # Cleanup
        for f in temp_files:
            try:
                os.remove(f)
            except:
                pass
    
    print(f"[SUSPICIOUS-FILE-{process_id}] Finished")

def burst_process(process_id, duration=60):
    """Simulates bursty CPU activity"""
    print(f"[SUSPICIOUS-BURST-{process_id}] ⚠️  Started at {datetime.now().strftime('%H:%M:%S')}")
    
    start_time = time.time()
    
    while time.time() - start_time < duration:
        # Burst of activity
        for _ in range(500000):
            _ = random.random() ** 2
        
        # Then idle
        time.sleep(3)
    
    print(f"[SUSPICIOUS-BURST-{process_id}] Finished")

def main():
    """
    Launch multiple processes to simulate system activity
    """
    print("=" * 60)
    print("🚀 PROCESS GENERATOR FOR CYBER THREAT MONITOR")
    print("=" * 60)
    print("\nThis will create various processes for testing.")
    print("Monitor them in your dashboard at http://localhost:8501\n")
    
    # Get user input
    print("Select process type to create:")
    print("1. Normal processes (3 processes, low resource usage)")
    print("2. Suspicious processes (mix of high CPU/memory/network)")
    print("3. Full simulation (5 normal + 5 suspicious)")
    print("4. Stress test (10+ processes)")
    print("5. Custom mix")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    duration = int(input("Duration in seconds (default 60): ") or "60")
    
    processes = []
    
    if choice == "1":
        # Normal processes only
        print("\n🟢 Creating 3 normal processes...")
        for i in range(3):
            p = multiprocessing.Process(target=normal_process, args=(i, duration))
            processes.append(p)
            p.start()
    
    elif choice == "2":
        # Suspicious processes only
        print("\n🔴 Creating suspicious processes...")
        suspicious_types = [
            (cpu_intensive_process, "CPU intensive"),
            (memory_intensive_process, "Memory intensive"),
            (network_simulator_process, "Network simulator"),
            (file_access_simulator, "File access"),
            (burst_process, "Burst activity")
        ]
        
        for i, (func, name) in enumerate(suspicious_types):
            print(f"  - {name}")
            p = multiprocessing.Process(target=func, args=(i, duration))
            processes.append(p)
            p.start()
    
    elif choice == "3":
        # Full simulation
        print("\n🎯 Creating full simulation (5 normal + 5 suspicious)...")
        
        # Normal processes
        for i in range(5):
            p = multiprocessing.Process(target=normal_process, args=(i, duration))
            processes.append(p)
            p.start()
        
        # Suspicious processes
        suspicious_funcs = [
            cpu_intensive_process,
            memory_intensive_process,
            network_simulator_process,
            file_access_simulator,
            burst_process
        ]
        
        for i, func in enumerate(suspicious_funcs):
            p = multiprocessing.Process(target=func, args=(i, duration))
            processes.append(p)
            p.start()
    
    elif choice == "4":
        # Stress test
        print("\n💥 Creating stress test (15 processes)...")
        
        # 5 normal
        for i in range(5):
            p = multiprocessing.Process(target=normal_process, args=(i, duration))
            processes.append(p)
            p.start()
        
        # 10 suspicious (mix of types)
        suspicious_funcs = [
            cpu_intensive_process,
            memory_intensive_process,
            network_simulator_process,
            file_access_simulator,
            burst_process
        ]
        
        for i in range(10):
            func = random.choice(suspicious_funcs)
            p = multiprocessing.Process(target=func, args=(i, duration))
            processes.append(p)
            p.start()
    
    elif choice == "5":
        # Custom mix
        num_normal = int(input("Number of normal processes: ") or "3")
        num_suspicious = int(input("Number of suspicious processes: ") or "3")
        
        print(f"\n🔧 Creating {num_normal} normal + {num_suspicious} suspicious processes...")
        
        for i in range(num_normal):
            p = multiprocessing.Process(target=normal_process, args=(i, duration))
            processes.append(p)
            p.start()
        
        suspicious_funcs = [
            cpu_intensive_process,
            memory_intensive_process,
            network_simulator_process,
            file_access_simulator,
            burst_process
        ]
        
        for i in range(num_suspicious):
            func = random.choice(suspicious_funcs)
            p = multiprocessing.Process(target=func, args=(i, duration))
            processes.append(p)
            p.start()
    
    else:
        print("❌ Invalid choice")
        return
    
    print(f"\n✅ {len(processes)} processes started!")
    print(f"⏱️  Running for {duration} seconds...")
    print("\n📊 Open your dashboard to see them: http://localhost:8501")
    print("   The dashboard will detect these processes and classify them!")
    print("\n⏳ Waiting for processes to complete...\n")
    
    # Wait for all processes
    for p in processes:
        p.join()
    
    print("\n" + "=" * 60)
    print("✅ All processes completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()