#!/usr/bin/python3

import ctfrecon

if __name__ == "__main__":
    results = []
    lines = ctfrecon.open_CSV('.exploitDB_results_index.csv')
    for line in lines:
        results.append(line.split(','))
    ctfrecon.display_results(results)
