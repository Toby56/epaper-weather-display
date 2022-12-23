function draw_temp_graph(temps) {
  const ctx = document.getElementById("today-graph-canvas");

  // Test data
  // var temps = [
  //   17, 17, 17, 16, 15, 15, 15, 15, 17, 19, 20, 21, 23, 24, 25, 26, 26, 26, 25,
  //   23, 21, 19, 18, 17, 16,
  // ];

  console.log(temps);

  var data = [];
  for (let i = 0; i < temps.length; i++) {
    data.push({ x: i, y: temps[i] });
  }

  var now_hour = new Date().getHours();
  var now_point = {
    x: now_hour,
    y: temps[now_hour],
  };

  new Chart(ctx, {
    data: {
      datasets: [
        {
          type: "line",
          data: data,
          borderWidth: 4,
          pointStyle: false,
          borderColor: "black",
          borderCapStyle: "round",
          cubicInterpolationMode: "default",
          tension: 0.5,
          order: 2,
        },
        {
          type: "scatter",
          data: [now_point],
          backgroundColor: "rgb(255, 0, 0)",
          borderWidth: 4,
          borderColor: "white",
          radius: 8,
        },
      ],
    },
    options: {
      maintainAspectRatio: false,
      animation: false,
      scales: {
        x: {
          type: "linear",
          display: false,
        },
        y: {
          display: false,
          // min: Math.min(...temps) - 2,
          max: Math.max(...temps) + 2,
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
}

document.addEventListener("DOMContentLoaded", (event) => {
  fetch("/todays-hourly-temps")
    .then((response) => response.json())
    .then((data) => draw_temp_graph(data));
});
