function draw_graph(temps) {
  const ctx = document.getElementById("today-graph-canvas");

  // Test data
  // var temps = [
  //   17, 17, 17, 16, 15, 15, 15, 15, 17, 19, 20, 21, 23, 24, 25, 26, 26, 26, 25,
  //   23, 21, 19, 18, 17, 16,
  // ];

  // Format list of numbers into {x, y} format
  var data = [];
  for (let i = 0; i <= temps.length; i++) {
    data.push({ x: i, y: temps[i] });
  }

  // Define a point at the current hour
  var now_hour = new Date().getHours();
  var now_point = {
    x: now_hour,
    y: temps[now_hour],
  };

  now_point_colour =
    "rgb(" +
    255 *
      ((temps[now_hour] - Math.min(...temps)) /
        (Math.max(...temps) - Math.min(...temps))) +
    ", 0, 0)";

  // Draw the graph!
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
          backgroundColor: now_point_colour,
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
          min: 0,
          max: temps.length,
        },
        y: {
          display: false,
          min: Math.min(...temps) - 2,
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

document.addEventListener("DOMContentLoaded", () => {
  fetch("/todays-hourly-temps")
    .then((response) => response.json())
    .then((data) => {
      draw_graph(data);
    });
});
