function draw_graph() {
  // Set up canvas element
  const canvas = document.getElementById("today-graph");
  const ctx = canvas.getContext("2d");

  canvas.width = canvas.clientWidth;
  canvas.height = canvas.clientHeight;

  // Load data from canvas data attribute
  var temps = JSON.parse(canvas.dataset.todayshourlytemps);

  // Test data
  // var temps = [
  //   17, 17, 17, 16, 15, 15, 15, 15, 17, 19, 20, 21, 23, 24, 25, 26, 26, 26, 25,
  //   23, 21, 19, 18, 17, 16,
  // ];
  // var temps = [1, 5, 4, 6, 4, 10];

  var tempsRange = Math.max(...temps) - Math.min(...temps);

  // Parameters
  let tension = 1;
  let lineWidth = 4;
  let nowPointDiameter = 7;
  let padding = nowPointDiameter;

  // Helper functions
  function pointAtDistanceAngle(p, d, a) {
    return {
      x: p.x + d * Math.cos(a),
      y: p.y + d * Math.sin(a),
    };
  }

  function distanceBetweenPoints(p1, p2) {
    return Math.sqrt(((p2.x - p1.x) ^ 2) + ((p2.y - p1.y) ^ 2));
  }

  function angleBetweenPoints(p1, p2) {
    return Math.atan((p2.y - p1.y) / (p2.x - p1.x));
  }

  function pointPos(index) {
    var temp = temps[index];

    x = padding + ((canvas.width - 2 * padding) / (temps.length - 1)) * index;
    y =
      canvas.height -
      (padding +
        ((canvas.height - 2 * padding) / tempsRange) *
          (temp - Math.min(...temps)));

    return { x: x, y: y };
  }

  // Draw the graph!
  ctx.lineWidth = lineWidth;
  ctx.lineCap = "round";
  ctx.beginPath();
  for (let i = 0; i < temps.length; i++) {
    if (i == 0) {
      point = pointPos(i);

      ctx.moveTo(point.x, point.y);
    } else {
      let prevPoint = pointPos(i - 1);
      let prevPrevPoint = pointPos(i != 1 ? i - 2 : i - 1);
      let currPoint = pointPos(i);
      let nextPoint = pointPos(i != temps.length - 1 ? i + 1 : i);

      let CP1Angle = angleBetweenPoints(prevPrevPoint, currPoint);
      let CP1Length = tension * distanceBetweenPoints(prevPoint, currPoint);
      let CP1 = pointAtDistanceAngle(prevPoint, CP1Length, CP1Angle);

      let CP2Angle = angleBetweenPoints(prevPoint, nextPoint);
      let CP2Length = -tension * distanceBetweenPoints(prevPoint, currPoint);
      let CP2 = pointAtDistanceAngle(currPoint, CP2Length, CP2Angle);

      ctx.bezierCurveTo(CP1.x, CP1.y, CP2.x, CP2.y, currPoint.x, currPoint.y);
    }
  }
  ctx.stroke();

  // Draw point at current hour
  var nowHour = new Date().getHours();
  var nowPoint = pointPos(nowHour, temps[nowHour]);

  nowPointColour =
    "rgb(" +
    255 * ((temps[nowHour] - Math.min(...temps)) / tempsRange) +
    ", 0, 0)";

  ctx.fillStyle = "white";
  ctx.beginPath();
  ctx.arc(nowPoint.x, nowPoint.y, nowPointDiameter + 4, 0, 2 * Math.PI);
  ctx.fill();

  ctx.fillStyle = nowPointColour;
  ctx.beginPath();
  ctx.arc(nowPoint.x, nowPoint.y, nowPointDiameter, 0, 2 * Math.PI);
  ctx.fill();
}

document.addEventListener("DOMContentLoaded", draw_graph);
