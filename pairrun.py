import time
import readchar

class PairRun:
    def __init__(self, loci_amount, mode="odd"):
        self.loci_amount = loci_amount

        if mode == "even":
            self.current_loci = 2
        elif mode == "odd":
            self.current_loci = 1
        else:
            raise ValueError("Error: Invalid mode | 'even' or 'odd' are the only options")

    def run(self):
        self.start_timer = time.perf_counter()
                
        while True:
            if self.current_loci > self.loci_amount:
                self.report()
                return None
            
            print(f"Loci: {self.current_loci}")
            
            self.user_input()

    def user_input(self):
        key = readchar.readkey()

        if key:
            self.current_loci += 2

    def report(self):
        stop_timer = time.perf_counter()
        total_time = stop_timer - self.start_timer
        avg_time = total_time / self.loci_amount

        print("\nGood job!")
        print("\n=== Stats ===")

        print(f"Total run time: {total_time:.2f}s")
        
        if self.loci_amount > 0:
            if avg_time <= 1.0:            
                print(f"Average time per loci (INCREDIBLE!): {(avg_time):.2f}s")

            elif avg_time <= 2.0:            
                print(f"Average time per loci (GOOD): {(avg_time):.2f}s")

            elif avg_time > 5.0:
                print(f"Average time per loci (COULD BE BETTER): {(avg_time):.2f}s")

        else:
            print("Average timer per loci: N/A")
