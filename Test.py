class MemorySegment:
    def __init__(self, size):
        self.size = size
        self.process = None  # Initially, no process is allocated

    def allocate(self, process):
        # Allocate memory to the process if the segment is free and large enough
        if process.size <= self.size and self.process is None:
            self.process = process
            return True
        return False

    def deallocate(self):
        # Deallocate the segment by removing the assigned process
        self.process = None

class Process:
    def __init__(self, size, name="Process"):
        self.size = size
        self.name = name

class QuickFitMemoryAllocator:
    def __init__(self, segment_sizes, common_sizes=[10, 20, 50, 100]):
        # Create memory segments of specified sizes
        self.memory_segments = [MemorySegment(size) for size in segment_sizes]
        # Initialize free lists for common-sized segments
        self.free_lists = {size: [] for size in common_sizes}

        # Populate free lists with memory segments of matching sizes
        for segment in self.memory_segments:
            for size in common_sizes:
                if segment.size == size:
                    self.free_lists[size].append(segment)
                    break

    def allocate_process(self, process):
        # Try to allocate memory from the free list of the matching size
        for size in sorted(self.free_lists.keys()):
            if process.size <= size and self.free_lists[size]:
                segment = self.free_lists[size].pop(0)
                if segment.allocate(process):
                    print(f"{process.name} allocated to segment of size {segment.size}.")
                    return True
        # If no exact fit is found, try to allocate from larger available segments
        for segment in self.memory_segments:
            if segment.size >= process.size and segment.process is None:
                segment.allocate(process)
                print(f"{process.name} allocated to segment of size {segment.size}.")
                return True
        print(f"No available memory for {process.name}.")
        return False

    def deallocate_process(self, process):
        # Deallocate the memory occupied by a process
        for segment in self.memory_segments:
            if segment.process == process:
                segment.deallocate()
                print(f"{process.name} deallocated from segment of size {segment.size}.")
                return True
        print(f"{process.name} not found in memory.")
        return False

    def display_memory(self):
        # Display the current memory layout with process assignments
        for segment in self.memory_segments:
            status = f"Occupied by {segment.process.name}" if segment.process else "Free"
            print(f"Segment size {segment.size}: {status}")


def get_input_processes():
    processes = []
    print("Define processes\n")
    num_processes = int(input("Enter the number of processes: "))
    for i in range(num_processes):
        size = int(input(f"Enter size for Process {i+1}: "))
        name = input(f"Enter name for Process {i+1}: ")
        processes.append(Process(size, name))
    return processes

def get_input_memory():
    memory_segments = []
    print("Define memory segments\n")
    num_segments = int(input("Enter the number of memory segments: "))
    for i in range(num_segments):
        size = int(input(f"Enter size for Memory Segment(16/32/64/128/256) {i+1}: "))
        memory_segments.append(size)
    return memory_segments

# Example usage
if __name__ == "__main__":
    # Get input from the user for processes and memory slots
    memory_segments = get_input_memory()
    processes = get_input_processes()

    # Create the memory allocator system
    allocator = QuickFitMemoryAllocator(memory_segments)

    # Display initial memory layout
    print("\nInitial Memory Layout:")
    allocator.display_memory()

    # Allocate processes
    print("\nAllocating Processes:")
    for process in processes:
        allocator.allocate_process(process)

    # Display memory after allocation
    print("\nMemory After Allocation:")
    allocator.display_memory()

    # Deallocate a process (optional)
    deallocate_process_name = input("\nEnter the name of the process to deallocate: ")
    for process in processes:
        if process.name == deallocate_process_name:
            allocator.deallocate_process(process)
            break

    # Display memory after deallocation
    print("\nMemory After Deallocation:")
    allocator.display_memory()
