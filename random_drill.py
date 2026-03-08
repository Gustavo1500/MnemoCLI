import random
import time
import readchar
from collections import defaultdict

class RandomDrill:
    def __init__(self, amount_loci, set_time_limit=True, standalone=False):
        self.amount_loci = amount_loci
        self.standalone = standalone

        # Time variables
        self.set_time_limit = set_time_limit
        if self.set_time_limit:
            self.time_limit = 2 # 2 seconds
        self.start_time = 0

        # Logging
        self.missed_loci = defaultdict(int)
        self.time_per_loci = defaultdict(list) # Assign time to each loci, example: Loci 14: times = 1.2, 2.1, 1.7 ...
        self.number = None
        self.episode_count = 0

    def generate_number(self):

        if self.number is not None:
            self.evaluate()

        self.start_time = 0
        self.start_time = time.perf_counter()

        prev_num = self.number

        self.number = random.randint(1, self.amount_loci)

        while self.number == prev_num:
            self.number = random.randint(1, self.amount_loci)

        self.episode_count += 1

        return self.number
    
    def evaluate(self):
        stop_time = time.perf_counter()
        actual_time = stop_time - self.start_time

        self.time_per_loci[self.number].append(actual_time)

        if actual_time > self.time_limit:
            self.missed_loci[self.number] += 1

    def user_input(self):
        while True:
            key = readchar.readkey()
            
            if key:
                self.episode_count += 1
                self.generate_number()
                break

    def generate_report(self):
        # ANSI Color Codes
        GREEN = '\033[42m'
        YELLOW = '\033[43m'
        RED = '\033[41m'
        GRAY = '\033[100m' # For loci never visited
        TEXT_DARK = '\033[30m'
        TEXT_LIGHT = '\033[97m'
        RESET = '\033[0m'

        print("\n" + "="*40)
        print("         DRILL HEATMAP REPORT")
        print("="*40)
        
        print(f"Legend: {GREEN} Fast {RESET} {YELLOW} Target {RESET} {RED} Slow {RESET} {GRAY} No Data {RESET}")
        print(f"Target Time: {self.time_limit}s\n")

        # We iterate through the full range of loci to ensure a consistent grid
        for i in range(1, self.amount_loci + 1):
            times = self.time_per_loci.get(i)
            
            if not times:
                # Locus was never visited during the random drill
                bg_color = GRAY
                text_color = TEXT_LIGHT
                display_time = " -- "
            else:
                avg = sum(times) / len(times)
                display_time = f"{avg:.1f}s"
                
                # Logic to determine color based on target time limit
                ratio = avg / self.time_limit
                if ratio < 0.8:
                    bg_color = GREEN
                    text_color = TEXT_DARK
                elif ratio <= 1.2:
                    bg_color = YELLOW
                    text_color = TEXT_DARK
                else:
                    bg_color = RED
                    text_color = TEXT_LIGHT

            # Print the formatted "tile"
            # Format: Locus ID on top, Avg time on bottom
            print(f"{bg_color}{text_color} {i:02d}:{display_time} {RESET}", end=" ")

            # Create a new row every 5 items for a grid layout
            if i % 5 == 0:
                print("\n")

        print("="*40)
        
        # Keep the summary stats below the heatmap
        print("\n- Top 3 Most Missed -")
        missed_sorted = sorted(self.missed_loci.items(), key=lambda x: x[1], reverse=True)
        if not missed_sorted:
            print("No misses recorded!")
        else:
            for loci, count in missed_sorted[:3]:
                print(f"Loci {loci}: {count} misses")
        print("="*40)
