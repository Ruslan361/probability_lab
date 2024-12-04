// ui.js

export function displayResultsTable(data, containerId, symbol = "x", precision = 4) {
    const container = document.getElementById(containerId);
    container.innerHTML = "";

    if (!data || !data.length) {
        container.innerHTML = "<p>No data to display</p>";
        return;
    }

    // Проверяем, является ли data массивом массивов (для многострочной таблицы)
    const isMultiRow = Array.isArray(data[0]);

    const table = document.createElement("table");
    const thead = table.createTHead();
    const headerRow = thead.insertRow();

    // Создаем заголовки столбцов
    let numColumns = isMultiRow ? data[0].length : data.length;
    for (let i = 0; i < numColumns; i++) {
        const th = document.createElement("th");
        th.innerHTML = symbol + `<sub>${i + 1}</sub>`;
        headerRow.appendChild(th);
    }

    const tbody = table.createTBody();

    // Заполняем таблицу данными
    if (isMultiRow) { // Многострочная таблица
        data.forEach(rowValues => {
            const row = tbody.insertRow();
            rowValues.forEach(value => {
                const td = row.insertCell();
                td.textContent = typeof value === "number" ? value.toFixed(precision) : value;
            });
        });

    } else { // Однострочная таблица

        const row = tbody.insertRow();
        data.forEach(value => {
            const td = row.insertCell();
            td.textContent = typeof value === "number" ? value.toFixed(precision) : value;
        });
    }

    container.appendChild(table);
}


export function displayMessage(message, containerId, className) {
    const container = document.getElementById(containerId);
    container.innerHTML = "";

    const div = document.createElement("div");
    div.className = className;
    div.textContent = message;
    container.appendChild(div);
}


export function displayPlot(plotUrl, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = "";

    if (!plotUrl) {
        container.innerHTML = "<p>No plot available</p>";
        return;
    }

    const img = document.createElement("img");
    img.src = `data:image/svg+xml;base64,${plotUrl}`;
    img.alt = "Plot"; // Добавьте более информативный alt текст
    img.style.width = "100%";

    container.appendChild(img);
}

export function removeElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
      setTimeout(() => {
        element.remove(); // Or element.style.display = 'none'; to just hide it
      }, 10000); // 10000 milliseconds = 10 seconds
    }
  }

export function displayResults2(z, pdfReal, pdfSelect, min, plotUrl, resultsContainerId = "results-table", plotContainerId = "hist") {
    const resultsContainer = document.getElementById(resultsContainerId);
    resultsContainer.innerHTML = "";

    if (!z || !z.length || !pdfReal || !pdfReal.length || !pdfSelect || !pdfSelect.length) {
        resultsContainer.innerHTML = "<p>No data to display</p>";
        return;
    }

    const createRow = (data) => {
        const row = document.createElement("tr");
        data.forEach(value => {
            const td = row.insertCell();
            td.textContent = value;
            row.appendChild(td);
        });
        return row;
    };

    const table = document.createElement("table");
    table.appendChild(createRow(z));
    table.appendChild(createRow(pdfReal));
    table.appendChild(createRow(pdfSelect));

    resultsContainer.appendChild(table);

    const p = document.createElement("p");
    p.textContent = `\\( \\max_{j=1, \\dots, k} \\left| \\frac{n_j}{n \\lvert \\Delta'_j \\rvert} - f_\\eta(z_j) \\right|= \\) ${min}`;
    resultsContainer.appendChild(p);

    displayPlot(plotUrl, plotContainerId);


    // Рендеринг LaTeX, если MathJax доступен
    if (typeof MathJax !== 'undefined') {
        MathJax.typeset();
    }

}

export function updateTable(labels, characteristics, containerId = "characteristic-of-numerical-distributions") {

    const container = document.getElementById(containerId);
    container.innerHTML = "";

    if (!labels || !characteristics || labels.length !== characteristics.length) {
        container.innerHTML = "<p>Invalid data received</p>";
        return;
    }

    const table = document.createElement("table");
    const thead = table.createTHead();
    const headerRow = thead.insertRow();

    labels.forEach(label => {
        const th = document.createElement("th");
        th.innerHTML = `\\( ${label} \\)`;
        headerRow.appendChild(th);
    });


    const tbody = table.createTBody();
    const row = tbody.insertRow();
    characteristics.forEach(value => {
        const td = row.insertCell();
        td.textContent = typeof value === "number" ? value.toFixed(5) : value;
        row.appendChild(td);
    });


    container.appendChild(table);

     // Рендеринг LaTeX, если MathJax доступен
    if (typeof MathJax !== 'undefined') {
        MathJax.typeset();
    }
}


export function clearError() {
    displayMessage("", "error-container", "error");
}

export function clearWarning() {
    displayMessage("", "warning-container", "warning");
}