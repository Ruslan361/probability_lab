import * as api from './api.js';
import * as ui from './ui.js';

let workTimes = [];
let mean = 0;
let disp = 0;
let isValid = false;

// --- Обработчик формы "start-form" ---
document.getElementById("start-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = await api.submitForm(Object.fromEntries(formData));

    if (data && !data.error) {
        isValid = true;
        workTimes = data.workTimes;
        mean = data.characteristics[0];
        disp = data.characteristics[3];

        ui.displayResultsTable(workTimes, "results");
        ui.updateTable(data.labels, data.characteristics);
        requestCDF(); // Вызываем requestCDF после успешного получения данных
    }
});


// --- Функция для запроса и отображения графика CDF ---
async function requestCDF() {
  if (isValid) {
      const data = await api.getCDF(workTimes, mean, disp);
      if (data && !data.error) {
          ui.displayPlot(data.plot_url, "cdf");
      }
  }
}


// --- Обработчик формы "interval-form" ---
document.getElementById("interval-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const numIntervals = parseFloat(document.getElementById("intervals").value);

    if (isValid) {
        const data = await api.getIntervalData(numIntervals, workTimes, mean, disp);
        if (data && !data.error) {
            ui.displayResults2(data.bin_centers, data.pdf_real, data.pdf_select, data.max_sub, data.graph_url);
        }
    }
});



// --- Обработчик формы "interval-form-2" ---
document.getElementById("interval-form-2").addEventListener("submit", async (event) => {
    event.preventDefault();

    const numIntervals = parseFloat(document.getElementById("intervals2").value);
    //const intervals = intervalsStr.split(',').map(Number).filter(num => !isNaN(num));
    const a = parseFloat(document.getElementById("a").value);



    if (isValid && numIntervals > 1) {
        const data = await api.getIntervalData2(numIntervals, a, workTimes, mean, disp);
        if (data && !data.error) {
           ui.displayResultsTable(data.q, "res-table", "q");

            const resultsContainer = document.getElementById("res-text");
            resultsContainer.innerHTML = ""; // Очищаем контейнер

            const createP = (text) => {
                const p = document.createElement("p");
                p.textContent = text;
                resultsContainer.appendChild(p);
            };


            createP(`\\( R_0 = \\)${data.R0}`);
            createP(`\\( \\overline{F}(R_0) = \\)${data.F}`);
            createP(data.message);


            if (typeof MathJax !== 'undefined') {
                MathJax.typeset(); // Для рендеринга LaTeX
            }
        }
    }
    else{
        ui.displayMessage("Неверный формат интервалов или значения ещё не определены", "error-container", "error");
    }
});