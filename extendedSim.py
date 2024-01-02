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

def simulate_24_hours(daily_attempts, hourly_proportions, avg_call_duration, channels):
    gos_results = []
    daily_traffic = np.sum(daily_attempts)

    for hour in range(24):
        attempts_per_hour = int(daily_traffic * hourly_proportions[hour])
        actual_gos = simulate_one_hour(attempts_per_hour, avg_call_duration, channels)
        gos_results.append(actual_gos)

    return np.mean(gos_results)

def run_simulation_24_hours(num_simulations, daily_attempts, hourly_proportions, avg_call_duration, channels):
    average_gos_results = []

    for _ in range(num_simulations):
        average_gos = simulate_24_hours(daily_attempts, hourly_proportions, avg_call_duration, channels)
        average_gos_results.append(average_gos)

    return average_gos_results

def main():
    hourly_proportions = [0.0009, 0.0005, 0.0004, 0.0004, 0.0008, 0.0044, 0.0168, 0.051, 0.0813, 0.0884, 0.0743, 0.0695, 0.0866, 0.0881, 0.09, 0.0848, 0.0721, 0.068, 0.047, 0.0406, 0.0183, 0.0095, 0.0043, 0.002]
    daily_attempts = 4444
    avg_call_duration = 2.5 / 60  # hours per call
    gos_target = 0.01  # 1%

    appropriate_channels = 25

    print(f"The appropriate number of voice channels is: {appropriate_channels}")
    num_simulations = 100
    average_gos_results = run_simulation_24_hours(num_simulations, daily_attempts, hourly_proportions, avg_call_duration, appropriate_channels)

    # Print average GOS result
    print(f"Average GOS over 24 hours: {np.mean(average_gos_results)}")
    
    # Plotting
    plt.hist(average_gos_results, bins=20, edgecolor='black')
    plt.xlabel('Average Grade of Service (GOS) over 24 hours')
    plt.ylabel('Frequency')
    plt.title('Monte Carlo Simulation of GOS over 24 hours')
    plt.show()

    

if __name__ == "__main__":
    main()
