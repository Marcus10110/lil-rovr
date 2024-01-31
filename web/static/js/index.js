document.getElementById("requestData").onclick = function () {
  fetch("/api/data")
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("data").textContent = JSON.stringify(data);
    });
};
