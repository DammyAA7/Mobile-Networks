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
    

def calculate_required_channels(offered_traffic, gos_target):
    channels = 1
    while erlang_b(offered_traffic, channels) > gos_target:
        channels += 1
    return channels


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

def simulate_24_hours_adjustable_channels(daily_attempts, hourly_proportions, avg_call_duration, gos_target):
    gos_results = []
    daily_traffic = np.sum(daily_attempts)
    total_energy_consumption = 0

    for hour in range(24):
        attempts_per_hour = int(daily_traffic * hourly_proportions[hour])
        
        offered_traffic = attempts_per_hour * avg_call_duration

        # Calculate required channels for the current hour
        required_channels = calculate_required_channels(offered_traffic, gos_target)


        
        actual_gos = simulate_one_hour(attempts_per_hour, avg_call_duration, required_channels)
        gos_results.append(actual_gos)

        # Calculate energy consumption for the current hour (proportional to the number of active channels)
        energy_consumption = required_channels
        total_energy_consumption += energy_consumption

    return np.mean(gos_results), total_energy_consumption

def run_simulation_24_hours_adjustable_channels(num_simulations, daily_attempts, hourly_proportions, avg_call_duration, gos_target):
    average_gos_results = []
    total_energy_consumption_results = []

    for _ in range(num_simulations):
        average_gos, total_energy_consumption = simulate_24_hours_adjustable_channels(daily_attempts, hourly_proportions, avg_call_duration, gos_target)
        average_gos_results.append(average_gos)
        total_energy_consumption_results.append(total_energy_consumption)

    return average_gos_results, total_energy_consumption_results


def main():
    hourly_proportions = [0.0009, 0.0005, 0.0004, 0.0004, 0.0008, 0.0044, 0.0168, 0.051, 0.0813, 0.0884, 0.0743, 0.0695, 0.0866, 0.0881, 0.09, 0.0848, 0.0721, 0.068, 0.047, 0.0406, 0.0183, 0.0095, 0.0043, 0.002]
    daily_attempts = 4444
    avg_call_duration = 2.5 / 60  # hours per call
    gos_target = 0.015  # 1.5%

    print("Simulation with fixed channels:")
    appropriate_channels = 25
    total_energy_consumption_fixed = appropriate_channels * 24
    num_simulations = 1000
    average_gos_results_fixed = run_simulation_24_hours(num_simulations, daily_attempts, hourly_proportions, avg_call_duration, appropriate_channels)
    print(f"Average GOS over 24 hours (fixed channels): {np.mean(average_gos_results_fixed)}")

    print("\nSimulation with adjustable channels:")
    average_gos_results_adjustable, total_energy_consumption_results_adjustable = run_simulation_24_hours_adjustable_channels(num_simulations, daily_attempts, hourly_proportions, avg_call_duration, gos_target)
    print(f"Average GOS over 24 hours (adjustable channels): {np.mean(average_gos_results_adjustable)}")

    energy_reduction_percentage = ((total_energy_consumption_fixed - np.mean(total_energy_consumption_results_adjustable)) / total_energy_consumption_fixed) * 100
    print(f"\nPercentage reduction in energy consumption: {energy_reduction_percentage:.2f}%")

    # Plotting
    plt.hist(average_gos_results_fixed, bins=20, edgecolor='black', alpha=0.5, label='Fixed Channels')
    plt.hist(average_gos_results_adjustable, bins=20, edgecolor='black', alpha=0.5, label='Adjustable Channels')
    plt.xlabel('Average Grade of Service (GOS) over 24 hours')
    plt.ylabel('Frequency')
    plt.title('Monte Carlo Simulation of GOS over 24 hours')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
