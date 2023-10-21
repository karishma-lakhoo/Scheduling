import sys
import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)


# Define the process data clas
class Process:
    def __init__(self, name, duration, arrival_time, io_frequency):
        self.name = name
        self.duration = duration
        self.arrival_time = arrival_time
        self.io_frequency = io_frequency
        self.start_time = -1
        self.end_time = -1


def stcf_scheduling(data_set):
    current_time = 0
    processes = list(data_set)
    output = ""

    while processes:
        ready_processes = [p for p in processes if p.arrival_time <= current_time]
        if ready_processes:
            shortest_process = min(ready_processes, key=lambda p: p.duration)
            processes.remove(shortest_process)

            # Start the process if it hasn't started yet
            if shortest_process.start_time == -1:
                shortest_process.start_time = current_time
                shortest_process.end_time = shortest_process.duration

            # Execute the process
            output += f"{shortest_process.name} "
            current_time += 1
            shortest_process.end_time -= 1

            # Check for I/O requests
            if shortest_process.end_time != 0:
                if shortest_process.io_frequency > 0 and (current_time - shortest_process.start_time) % shortest_process.io_frequency == 0:
                    output += f"!{shortest_process.name} "

            # Update the duration of the executed process
            shortest_process.duration -= 1

            # If the process is not completed, put it back in the list
            if shortest_process.duration > 0:
                processes.append(shortest_process)

        else:
            # No ready processes, time passes
            current_time += 1

    return output


def main():
    # Check if the correct number of arguments is provided
    import sys
    if len(sys.argv) != 2:
        return 1

    # Extract the input file name from the command line arguments
    input_file_name = f"Process_List/{config['dataset']}/{sys.argv[1]}"

    # Define the number of processes
    num_processes = 0

    # Initialize an empty list for process data
    data_set = []

    # Open the file for reading
    try:
        with open(input_file_name, "r") as file:
            # Read the number of processes from the file
            num_processes = int(file.readline().strip())

            # Read process data from the file and populate the data_set list
            for _ in range(num_processes):
                line = file.readline().strip()
                name, duration, arrival_time, io_frequency = line.split(',')
                process = Process(name, int(duration), int(arrival_time), int(io_frequency))
                data_set.append(process)

    except FileNotFoundError:
        print("Error opening the file.")
        return 1

    """
    TODO Your Algorithm - assign your output to the output variable
    """

    # output = "AB AC AB !AD BA CB !BL BX AB" #Example output
    output = stcf_scheduling(data_set)

    """
    End of your algorithm
    """

    # Open a file for writing
    try:
        output_path = f"Schedulers/template/{config['dataset']}/template_out_{sys.argv[1].split('_')[1]}"
        with open(output_path, "w") as output_file:
            # Write the final result to the output file
            output_file.write(output)

    except IOError:
        print("Error opening the output file.")
        return 1

    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)