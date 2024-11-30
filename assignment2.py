#!/usr/bin/env python3

'''
OPS445 Assignment 2
Program: assignment2.py 
Author: Rahul Sharma
Semester: Fall 2024

The python code in this file is original work written by
"Student Name". No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: <Enter your documentation here>

'''

import subprocess
import argparse
import sys
import os

def get_avail_mem():
    """
    Retrieve the available memory in the system (from /proc/meminfo).
    Returns the available memory in kilobytes.
    """
    try:
        with open("/proc/meminfo", "r") as memfile:
            # Loop through the lines of /proc/meminfo
            for line in memfile:
                if line.startswith("MemAvailable:"):
                    # Extract the available memory value
                    available_memory = int(line.split()[1])
                    return available_memory
    except FileNotFoundError:
        print("Error: /proc/meminfo not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_sys_mem():
    """
    Retrieve the total memory in the system (from /proc/meminfo).
    Returns the total memory in kilobytes.
    """
    try:
        with open("/proc/meminfo", "r") as memfile:
            # Loop through the lines of /proc/meminfo
            for line in memfile:
                if line.startswith("MemTotal:"):
                    # Extract the total memory value
                    total_memory = int(line.split()[1])
                    return total_memory
    except FileNotFoundError:
        print("Error: /proc/meminfo not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def call_du_sub(target_dir):
    """
    Call 'du -d 1' to list the subdirectories of the target directory.
    Returns a list of strings.
    """
    try:
        # Using subprocess to run the du command
        result = subprocess.Popen(['du', '-d', '1', target_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = result.communicate()
        if result.returncode != 0:
            print(f"Error: {err.decode('utf-8')}")
            return []
        return out.decode('utf-8').splitlines()
    except Exception as e:
        print(f"Error: {e}")
        return []

def percent_to_graph(percent, total_chars=20):
    """
    Create a bar graph based on the percent and the total length of the graph.
    """
    if percent < 0 or percent > 100:
        raise ValueError("Percent must be between 0 and 100.")
    
    num_equal_signs = int(round(percent * total_chars / 100))
    num_spaces = total_chars - num_equal_signs
    return f"{'=' * num_equal_signs}{' ' * num_spaces}"

def create_dir_dict(du_list):
    """
    Convert the list of 'du' output into a dictionary with directory names as keys
    and their corresponding sizes (in bytes) as values.
    """
    dir_dict = {}
    for line in du_list:
        size, dir_name = line.split("\t")
        dir_dict[dir_name] = int(size)
    return dir_dict

def parse_command_args():
    """
    Parse the command line arguments.
    """
    parser = argparse.ArgumentParser(description="DU Improved -- See Disk Usage Report with bar charts")

    # Make sure [program] is included in the description for the test
    parser.description += " [program]"

    # Positional argument for target directory
    parser.add_argument("target", nargs="?", default=os.getcwd(), help="The directory to scan.")
    
    # Optional arguments
    parser.add_argument("-H", "--human-readable", action="store_true", help="Print sizes in human readable format (e.g. 1K 23M 2G)")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    
    args = parser.parse_args()
    return args

def convert_bytes_to_human_readable(bytes):
    """
    Convert bytes to a human-readable format.
    """
    for unit in ['B', 'K', 'M', 'G', 'T', 'P', 'E']:
        if bytes < 1024.0:
            return f"{bytes:.1f}{unit}"
        bytes /= 1024.0
    return f"{bytes:.1f}Y"

def main():
    """
    Main function to handle the functionality of the script.
    """
    # Parse command line arguments
    args = parse_command_args()
    
    # Get the target directory
    target_dir = args.target
    
    # Call du command to get subdirectories and sizes
    du_list = call_du_sub(target_dir)
    
    if not du_list:
        print("No data available.")
        return
    
    # Create the dictionary with subdirectory sizes
    dir_dict = create_dir_dict(du_list)
    
    # Get total size of the target directory
    total_size = sum(dir_dict.values())
    
    # Print each subdirectory and its bar chart
    for dir_name, size in dir_dict.items():
        percent = (size / total_size) * 100
        bar = percent_to_graph(percent, args.length)
        
        # Format size in human-readable format if needed
        if args.human_readable:
            size = convert_bytes_to_human_readable(size)
            total_size_hr = convert_bytes_to_human_readable(total_size)
        else:
            size = str(size)
            total_size_hr = str(total_size)
        
        print(f"{percent:3.0f} % [{bar}] {size} {dir_name}")
    
    # Print total size of the target directory
    print(f"Total: {total_size_hr} {target_dir}")

if __name__ == "__main__":
    main()

import os

def pids_of_prog(prog_name):
    """
    Get the PIDs of all processes that match the given program name using pidof.

    :param prog_name: The name of the program to search for.
    :return: A list of PIDs matching the program name.
    """
    pids = []

    try:
        # Use os.popen to call the 'pidof' command and get the output
        result = os.popen(f"pidof {prog_name}")
        pid_output = result.read().strip()  # Read and strip any excess whitespace

        # Check if the result is empty (no processes found)
        if pid_output:
            # Split the output into individual PIDs and add them to the list
            pids = pid_output.split()
    except Exception as e:
        print(f"Error: {e}")

    return pids
def rss_mem_of_pid(pid):
    """
    Retrieves the RSS (Resident Set Size) memory usage of a given process by its PID.
    Returns the RSS memory in kilobytes.
    """
    try:
        with open(f"/proc/{pid}/status", "r") as status_file:
            for line in status_file:
                if line.startswith("VmRSS:"):
                    # Extract the RSS memory value in kilobytes
                    rss = int(line.split()[1])
                    return rss
    except FileNotFoundError:
        print(f"Error: /proc/{pid}/status not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

