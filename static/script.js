document.addEventListener("DOMContentLoaded", (event) => {
  const ctx = document.getElementById("today-graph-canvas");

  var numbers = [
    17, 17, 17, 16, 15, 15, 15, 15, 17, 19, 20, 21, 23, 24, 25, 26, 26, 26, 25,
    23, 21, 19, 18, 17, 16,
  ];

  var data = [];

  for (let i = 0; i < numbers.length; i++) {
    data.push({ x: i, y: numbers[i] });
  }

  new Chart(ctx, {
    data: {
      datasets: [
        {
          type: "line",
          order: 2,
          data: data,
        },
        {
          type: "bar",
          maxBarThickness: 12,
          data: [{ x: "12", y: Math.max(...numbers) }],
        },
      ],
    },
    options: {
      maintainAspectRatio: false,
      animation: false,
      scales: {
        x: {
          display: false,
          type: "linear",
          ticks: {
            display: false,
            color: "black",
            maxRotation: 0,
            font: {
              size: 16,
              family: "Rubik, sans-serif",
            },
          },
          border: {
            display: false,
          },
          grid: {
            tickLength: 0,
            color: "black",
            display: false,
          },
        },
        y: {
          display: false,
          min: Math.min(...numbers) - 1,
          max: Math.max(...numbers) + 1,
        },
      },
      elements: {
        point: {
          pointStyle: false,
        },
        line: {
          borderWidth: 4,
          borderColor: "black",
          borderCapStyle: "round",
          cubicInterpolationMode: "default",
          tension: 0.5,
        },
        bar: {
          borderRadius: 6,
          borderWidth: 4,
          borderColor: "white",
          backgroundColor: "black",
          zIndex: 2,
        },
      },
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          enabled: false,
        },
      },
    },
  });
});
