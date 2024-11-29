const form = document.getElementById("start-form");
let workTimes = [];
let mean = 0;
let disp = 0;
let isvalid = false;
form.onsubmit = (event) => {
    event.preventDefault();

    const formData = new FormData(form);

    fetch('/submit', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            // Если есть ошибка, отображаем её
            displayError(data.error);
            isvalid = false;
        } else {
            // Если всё успешно, выводим результаты
            displayResults(data.workTimes);
            workTimes = data.workTimes
            updateTable(data.labels, data.characteristics);
            console.log(data.characteristics);
            mean = data.characteristics[0];
            disp = data.characteristics[3];
            isvalid = true;
            requestCDF(data.workTimes, data.characteristics[0], data.characteristics[3]);
            clearError(); // Убираем старые ошибки
        }

        if (data.warning) {
            // Если есть предупреждение, отображаем его
            displayWarning(data.warning);
        } else {
            clearWarning(); // Убираем старые предупреждения
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
};

function displayResults(data) {
    const resultsContainer = document.getElementById("results");
    resultsContainer.innerHTML = ""; // Очистить старые результаты

    if (!data || !data.length) {
        resultsContainer.innerHTML = "<p>No data to display</p>";
        return;
    }

    // Создать таблицу
    const table = document.createElement("table");

    // Создать заголовок таблицы
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");
    data.forEach((_, index) => {
        const th = document.createElement("th");
        th.innerHTML = `x<sub>${index + 1}</sub>`;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Создать тело таблицы
    const tbody = document.createElement("tbody");
    const row = document.createElement("tr");
    data.forEach(value => {
        const td = document.createElement("td");
        if (typeof value === "number") {
            td.textContent = value.toFixed(4); // Форматировать числа
        } else {
            td.textContent = value; // Вывести строку как есть
        }
        row.appendChild(td);
    });
    tbody.appendChild(row);
    table.appendChild(tbody);

    // Добавить таблицу в контейнер
    resultsContainer.appendChild(table);
}

// Функция для отображения ошибок
function displayError(message) {
    const errorContainer = document.getElementById("error-container");
    errorContainer.innerHTML = ""; // Очистить предыдущие ошибки

    const errorDiv = document.createElement("div");
    errorDiv.className = "error";
    errorDiv.textContent = message;

    errorContainer.appendChild(errorDiv);
}

// Функция для очистки ошибок
function clearError() {
    const errorContainer = document.getElementById("error-container");
    errorContainer.innerHTML = "";
}

// Функция для отображения предупреждений
function displayWarning(message) {
    const warningContainer = document.getElementById("warning-container");
    warningContainer.innerHTML = ""; // Очистить предыдущие предупреждения

    const warningDiv = document.createElement("div");
    warningDiv.className = "warning";
    warningDiv.textContent = message;

    warningContainer.appendChild(warningDiv);
}

// Функция для очистки предупреждений
function clearWarning() {
    const warningContainer = document.getElementById("warning-container");
    warningContainer.innerHTML = "";
}

// Функция для обновления таблицы
function updateTable(labels, characteristics) {
    const resultsContainer = document.getElementById("characteristic-of-numerical-distributions");
    resultsContainer.innerHTML = ""; // Очистить старые данные

    if (!labels || !characteristics || labels.length !== characteristics.length) {
        resultsContainer.innerHTML = "<p>Invalid data received</p>";
        return;
    }

    // Создать таблицу
    const table = document.createElement("table");

    // Создать заголовок таблицы
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");
    labels.forEach(label => {
        const th = document.createElement("th");
        th.innerHTML = `\\( ${label} \\)`; // Для LaTeX-рендеринга
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Создать тело таблицы
    const tbody = document.createElement("tbody");
    const row = document.createElement("tr");
    characteristics.forEach(value => {
        const td = document.createElement("td");
        if (typeof value === "number") {
            td.textContent = value.toFixed(5); // Форматировать числа
        } else {
            td.textContent = value; // Вывести строку как есть
        }
        row.appendChild(td);
    });
    tbody.appendChild(row);
    table.appendChild(tbody);

    // Добавить таблицу в контейнер
    resultsContainer.appendChild(table);

    // Обновить MathJax для рендеринга LaTeX
    if (window.MathJax) {
        MathJax.typeset();
    }
}

// Функция для отображения гистограммы
function displayPlot(plotUrl, id) {
    const plotContainer = document.getElementById(id);
    plotContainer.innerHTML = ""; // Очистить старый график

    if (!plotUrl) {
        plotContainer.innerHTML = "<p>No plot available</p>";
        return;
    }

    const img = document.createElement("img");
    img.src = `data:image/svg+xml;base64,${plotUrl}`;
    img.alt = "Гистограмма относительных частот";
    img.style.width = "100%"; // Адаптация под контейнер

    plotContainer.appendChild(img);
}

function requestCDF(workTimes, mean, disp) {
    if (isvalid) {
        fetch('/cdf-plot', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ workTimes, mean, disp}),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                displayError(data.error); // Отобразить ошибку
            } else {
                displayPlot(data.plot_url, "cdf"); // Отобразить график
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
    }
}

function displayResults2(z, pdf_real, pdf_select, min, plotUrl) {
    const resultsContainer = document.getElementById("results-table");
    resultsContainer.innerHTML = ""; // Очистить старые результаты

    if (!z || !z.length || !pdf_real || !pdf_real.length || !pdf_select.length || !pdf_select) {
        resultsContainer.innerHTML = "<p>No data to display</p>";
        return;
    }

    // Создать таблицу для результатов
    const table = document.createElement("table");
    const tbody = document.createElement("tbody");

    // Создать строку с данными
    row = create_row(z);
    tbody.appendChild(row);
    table.appendChild(tbody);

    row = create_row(pdf_real);
    tbody.appendChild(row);
    table.appendChild(tbody);
    resultsContainer.appendChild(table);

    row = create_row(pdf_select);
    tbody.appendChild(row);
    table.appendChild(tbody);
    resultsContainer.appendChild(table);

    p = document.createElement("p")
    p.textContent = "\\( \\max_{j=1, \\dots, k} \\left| \\frac{n_j}{n \\lvert \\Delta'_j \\rvert} - f_\\eta(z_j) \\right|= \\) " + String(min)
    resultsContainer.appendChild(p);
    function create_row(z) {
        const row = document.createElement("tr");
        z.forEach(value => {
            const td = document.createElement("td");
            td.textContent = value;
            row.appendChild(td);
        });
        return row;
    }
    displayPlot(plotUrl, "hist");

    if (window.MathJax) {
        MathJax.typeset();
    }
}


document.getElementById("interval-form").addEventListener("submit", function (event) {
    event.preventDefault(); // Останавливаем обычную отправку формы

    // Получаем введенные интервалы как строку
    const intervalsStr = document.getElementById("intervals").value;

    // Преобразуем строку в массив чисел
    const intervals = intervalsStr.split(',').map(item => parseFloat(item.trim()));

    // Проверяем, чтобы интервалы были числами и их было больше 1
    if (intervals.length < 2 || intervals.some(isNaN)) {
        displayError("Неверный формат интервалов. Пожалуйста, введите числа.");
        return;
    }

    // Генерация данных для работы (пример)
    //const workTimes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 10]; // Пример данных
    //const min = Math.min(workTimes);
    //const max = Math.max(workTimes);

    // Отправка данных на сервер для получения результатов
    if (isvalid) {
        const formData = new FormData();
        formData.append("intervals", JSON.stringify(intervals));
        formData.append("workTimes", JSON.stringify(workTimes));
        formData.append("mean", JSON.stringify(mean));
        formData.append("disp", JSON.stringify(disp));

        fetch("/interval", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                displayError(data.error);
            } else {
                //z, pdf_real, pdf_select
                displayResults2(data.bin_centers, data.pdf_real, data.pdf_select, data.max_sub, data.graph_url);
                clearError(); // Убираем старые ошибки
            }

            if (data.warning) {
                displayWarning(data.warning);
            } else {
                clearWarning(); // Убираем старые предупреждения
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
    }
});
