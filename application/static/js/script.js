const form = document.getElementById("start-form");

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
        } else {
            // Если всё успешно, выводим результаты
            displayResults(data.workTimes);
            updateTable(data.labels, data.characteristics);
            console.log(data.characteristics)
            requestCDF(data.workTimes, data.characteristics[0], data.characteristics[3])
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

