import numpy as np

def compute_histogram(data, bin_edges, density=False, cumulative=False):
    data = np.array(data)
    hist_values = np.zeros(len(bin_edges) - 1)

    for value in data:
        for i in range(len(bin_edges) - 1):
            if bin_edges[i] <= value and (value < bin_edges[i + 1] or (i == len(bin_edges) - 2 and value <= bin_edges[i + 1])):
                hist_values[i] += 1
                break

    if cumulative:
        hist_values = np.cumsum(hist_values)

    if density:
        total_count = data.shape[0]
        if cumulative:  # Нормировка для cumulative density
            hist_values = hist_values / total_count
        else:  # Нормировка для обычной density
            bin_widths = np.diff(bin_edges)
            hist_values = hist_values / (total_count * bin_widths)

    bin_centers = [(bin_edges[i] + bin_edges[i + 1]) / 2 for i in range(len(bin_edges) - 1)]

    return hist_values, bin_centers