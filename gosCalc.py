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

def main():
    attempts_per_hour = 400
    avg_call_duration = 2.5 / 60  # hours per call
    offered_traffic = attempts_per_hour * avg_call_duration
    gos_target = 0.01  # 1%

    appropriate_channels = find_appropriate_channels(attempts_per_hour, avg_call_duration, gos_target)

    if appropriate_channels is not None:
        print(f"The appropriate number of voice channels is: {appropriate_channels}")
    else:
        print("No appropriate number of channels found within the specified range.")

    channels_range = range(1, 51)  # Adjust the range based on your requirements
    gos_values = []

    for channels in channels_range:
        gos = erlang_b(offered_traffic, channels)
        gos_values.append(gos)

    # Plotting
    plt.plot(channels_range, gos_values)
    plt.xlabel('Number of Voice Channels')
    plt.ylabel('Grade of Service (GOS)')
    plt.title('Erlang-B GOS for a Cell Site')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
