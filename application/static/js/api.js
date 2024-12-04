import * as ui from './ui.js';
function createFormData(data) {
    const formData = new FormData();
    for (const [key, value] of Object.entries(data)) {
        formData.append(key, value);
    }
    return formData;
}
async function fetchData(url, data) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();

        if (result.error) {
            ui.displayMessage(result.error, "error-container", "error"); // Предполагается, что displayMessage определена в другом модуле
            return { error: result.error }; // Возвращаем ошибку для обработки в вызывающей функции
        }

        if (result.warning) {
            ui.displayMessage(result.warning, "warning-container", "warning"); // Аналогично для предупреждений
        }

        return result; // Возвращаем данные без ошибок

    } catch (error) {
        console.error("Error:", error);
        ui.displayMessage("Ошибка при обращении к серверу.", "error-container", "error"); // Общее сообщение об ошибке
        return { error: "Ошибка при обращении к серверу." }; // Возвращаем ошибку
    }
}

export async function submitForm(formData) {
    return await fetchData('/submit', formData);
}

export async function getCDF(workTimes, mean, disp) {
    return await fetchData('/cdf-plot', { workTimes, mean, disp });
}

export async function getIntervalData(intervals, workTimes, mean, disp) {
    return await fetchData("/interval", { intervals, workTimes, mean, disp });
}

export async function getIntervalData2(intervals, a, workTimes, mean, disp) {
    return await fetchData("/intervals2", { intervals, a, workTimes, mean, disp });
}

// // Экспортируем вспомогательную функцию для обработки FormData (если нужно)
// export function createFormData(data) {
//     const formData = new FormData();
//     for (const key in data) {
//         formData.append(key, JSON.stringify(data[key]));
//     }
//     return formData;
// }