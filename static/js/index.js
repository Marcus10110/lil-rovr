async function drive(speed, direction) {
  console.log(`Driving at speed ${speed} in direction ${direction}`);
  const url = `/api/drive?speed=${speed.toFixed(
    3
  )}&direction=${direction.toFixed(3)}`;
  console.log(`URL: ${url}`);
  const start = Date.now();
  await fetch(url);
  const end = Date.now();
  console.log(`Request took ${end - start}ms`);
}

document.getElementById("requestData").onclick = function () {
  drive(0.1, 45);
};

const haveEvents = "ongamepadconnected" in window;
const controllers = {};

function connecthandler(e) {
  addgamepad(e.gamepad);
}

function addgamepad(gamepad) {
  controllers[gamepad.index] = gamepad;

  const d = document.createElement("div");
  d.setAttribute("id", `controller${gamepad.index}`);

  const t = document.createElement("h1");
  t.textContent = `gamepad: ${gamepad.id}`;
  d.appendChild(t);

  const b = document.createElement("ul");
  b.className = "buttons";
  gamepad.buttons.forEach((button, i) => {
    const e = document.createElement("li");
    e.className = "button";
    e.textContent = `Button ${i}`;
    b.appendChild(e);
  });

  d.appendChild(b);

  const a = document.createElement("div");
  a.className = "axes";

  gamepad.axes.forEach((axis, i) => {
    const p = document.createElement("progress");
    p.className = "axis";
    p.setAttribute("max", "2");
    p.setAttribute("value", "1");
    p.textContent = i;
    a.appendChild(p);
  });

  d.appendChild(a);

  // See https://github.com/luser/gamepadtest/blob/master/index.html
  const start = document.getElementById("start");
  if (start) {
    start.style.display = "none";
  }

  document.body.appendChild(d);
  scheduleUpdate();
}

function scheduleUpdate() {
  // requestAnimationFrame(updateStatus);
  setTimeout(updateStatus, 1000 / 15);
}

function disconnecthandler(e) {
  removegamepad(e.gamepad);
}

function removegamepad(gamepad) {
  const d = document.getElementById(`controller${gamepad.index}`);
  document.body.removeChild(d);
  delete controllers[gamepad.index];
}

async function updateStatus() {
  if (!haveEvents) {
    scangamepads();
  }

  // handle sending data to backend:
  // get first controller if it exists:
  const controllersArray = Object.entries(controllers);

  if (controllersArray.length >= 1) {
    const firstController = controllersArray[0][1];
    let speed = firstController.axes[1];
    let direction = firstController.axes[0];
    // axis are -1 to +1;
    direction *= -90;
    speed *= -1;
    await drive(
      Math.round(speed * 1000) / 1000,
      Math.round(direction * 1000) / 1000
    );
  }

  controllersArray.forEach(([i, controller]) => {
    const d = document.getElementById(`controller${i}`);
    const buttons = d.getElementsByClassName("button");

    controller.buttons.forEach((button, i) => {
      const b = buttons[i];
      let pressed = button === 1.0;
      let val = button;

      if (typeof button === "object") {
        pressed = val.pressed;
        val = val.value;
      }

      const pct = `${Math.round(val * 100)}%`;
      b.style.backgroundSize = `${pct} ${pct}`;
      b.textContent = pressed ? `Button ${i} [PRESSED]` : `Button ${i}`;
      b.style.color = pressed ? "#42f593" : "#2e2d33";
      b.className = pressed ? "button pressed" : "button";
    });

    const axes = d.getElementsByClassName("axis");
    controller.axes.forEach((axis, i) => {
      const a = axes[i];
      a.textContent = `${i}: ${axis.toFixed(4)}`;
      a.setAttribute("value", axis + 1);
    });
  });

  scheduleUpdate();
}

function scangamepads() {
  const gamepads = navigator.getGamepads();
  document.querySelector("#noDevices").style.display = gamepads.filter(Boolean)
    .length
    ? "none"
    : "block";
  for (const gamepad of gamepads) {
    if (gamepad) {
      // Can be null if disconnected during the session
      if (gamepad.index in controllers) {
        controllers[gamepad.index] = gamepad;
      } else {
        addgamepad(gamepad);
      }
    }
  }
}

if (!haveEvents) {
  setInterval(scangamepads, 500);
} else {
  window.addEventListener("gamepadconnected", connecthandler);
  window.addEventListener("gamepaddisconnected", disconnecthandler);
}
