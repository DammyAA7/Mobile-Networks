import numpy as np
import matplotlib.pyplot as plt

def erlang_b(traffic, channels):
    """
    Calculate Erlang-B formula for grade of service.

    Parameters:
    - traffic: Offered traffic (in erlangs)
    - channels: Number of voice channels

    Returns:
    - Grade of Service
    """
    numerator = (traffic ** channels) / factorial(channels)
    denominator = sum([(traffic ** i) / factorial(i) for i in range(channels + 1)])
    return numerator / denominator

def factorial(n):
    """
    Calculate factorial of a number.

    Parameters:
    - n: Integer

    Returns:
    - Factorial of n
    """
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
    
def find_appropriate_channels(attempts_per_hour, avg_call_duration, gos_target):
    offered_traffic = attempts_per_hour * avg_call_duration

    channels_range = range(1, 51)
    for channels in channels_range:
        gos = erlang_b(offered_traffic, channels)
        print(f"Channels: {channels}, GOS: {gos}")

        if gos < gos_target:
            return channels

    return None

def simulate_one_hour(attempts_per_hour, avg_call_duration, channels):
    offered_traffic = attempts_per_hour * avg_call_duration
    dropped_calls = 0

    call_start_times = np.sort(np.random.uniform(0, 1, attempts_per_hour))  # Uniform distribution for call start times
    call_durations = np.random.exponential(avg_call_duration, attempts_per_hour)  # Exponential distribution for call durations

    for start_time, duration in zip(call_start_times, call_durations):
        end_time = start_time + duration
        gos = erlang_b(offered_traffic, channels)

        if end_time > 1 or np.random.rand() > gos:
            dropped_calls += 1

    actual_gos = (attempts_per_hour - dropped_calls) / attempts_per_hour
    return actual_gos

def run_simulation(num_simulations, attempts_per_hour, avg_call_duration, channels):
    gos_results = []

    for _ in range(num_simulations):
        actual_gos = simulate_one_hour(attempts_per_hour, avg_call_duration, channels)
        gos_results.append(actual_gos)

    return gos_results

def main():
    attempts_per_hour = 400
    avg_call_duration = 2.5 / 60  # hours per call
    gos_target = 0.01  # 1%

    appropriate_channels = find_appropriate_channels(attempts_per_hour, avg_call_duration, gos_target)

    if appropriate_channels is not None:
        print(f"The appropriate number of voice channels is: {appropriate_channels}")
        num_simulations = 1000
        gos_results = run_simulation(num_simulations, attempts_per_hour, avg_call_duration, appropriate_channels)

        # Plotting
        plt.hist(gos_results, bins=20, edgecolor='black')
        plt.xlabel('Actual Grade of Service (GOS)')
        plt.ylabel('Frequency')
        plt.title('Monte Carlo Simulation of GOS')
        plt.show()

    else:
        print("No appropriate number of channels found within the specified range.")

if __name__ == "__main__":
    main()
