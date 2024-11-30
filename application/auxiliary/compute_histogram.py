import numpy as np


def compute_histogram_with_intervals_manual(data, bin_edges, density=False, cumulative=False):
    """
    Вычисляет значения гистограммы для данных с использованием циклов, без использования np.histogram.
    
    :param data: Список или массив данных для гистограммы.
    :param bin_edges: Массив с границами интервалов.
    :param density: Если True, гистограмма будет нормализована (относительная частота).
    :param cumulative: Если True, гистограмма будет накопительной.
    
    :return: (values, bin_centers) - значения гистограммы и середины интервалов.
    """
    
    # Преобразуем data в numpy-массив для более быстрого вычисления
    data = np.array(data)
    #hist_values, _ = plt.hist(data, bins='auto', cumulative=True, density=True)

    #Инициализируем массив для значений гистограммы
    hist_values = np.zeros(len(bin_edges) - 1)
    
    # Цикл по каждому элементу данных
    for value in data:
        # Для каждого значения находим, в какой интервал оно попадает
        for i in range(len(bin_edges) - 1):
            if bin_edges[i] <= value and value < bin_edges[i + 1]:
                hist_values[i] += 1
                break
    

    
    #Если нужно накопительное распределение (cumulative=True)
    if cumulative:
        hist_values = np.cumsum(hist_values)

    # Нормализация по желанию (density=True)
    if density and cumulative:
        total_count = data.shape[0]
        bin_widths = np.diff(bin_edges)
        # hist_values = hist_values / (total_count * bin_widths)
        hist_values = hist_values / total_count
    if density and not cumulative:
        total_count = data.shape[0]
        bin_widths = np.diff(bin_edges)
        hist_values = hist_values / (total_count * bin_widths)
    
    # Вычисляем середины интервалов
    bin_centers = [(bin_edges[i] + bin_edges[i + 1]) / 2 for i in range(len(bin_edges) - 1)]
    
    return hist_values, bin_centers