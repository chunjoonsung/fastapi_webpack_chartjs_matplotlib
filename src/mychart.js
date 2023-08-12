
export const drawChart = function(id,type,data) {
    const chrt = document.getElementById(id).getContext("2d");
    return new Chart(chrt, {
        type: type,
        data: data,
        options: {
            responsive: false,
        },
    });
}

