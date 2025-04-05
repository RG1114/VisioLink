const express = require("express");
const { exec } = require("child_process");
const path = require("path");
const cors = require("cors");

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

// We no longer serve the IP from here; forward.py handles that.
// Uncomment below if you plan to serve a build in production.
// app.use(express.static(path.join(__dirname, "build")));
// app.get("*", (req, res) => {
//   res.sendFile(path.join(__dirname, "build", "index.html"));
// });

// Track camera process
let cameraProcess = null;

app.get("/start-camera", (req, res) => {
  try {
    if (cameraProcess) {
      return res.status(400).json({ message: "Camera is already running" });
    }
    console.log("Starting camera process...");
    cameraProcess = exec("python run_gesture_model.py", (error, stdout, stderr) => {
      if (error) {
        console.error(`Camera process error: ${error.message}`);
        return;
      }
      if (stderr) {
        console.error(`Camera process stderr: ${stderr}`);
        return;
      }
      console.log(`Camera process stdout: ${stdout}`);
    });
    cameraProcess.on("exit", (code) => {
      console.log(`Camera process exited with code ${code}`);
      cameraProcess = null;
    });
    res.status(200).json({ message: "Camera started successfully" });
  } catch (error) {
    console.error("Error starting camera:", error);
    res.status(500).json({ error: "Failed to start camera" });
  }
});

app.get("/stop-camera", (req, res) => {
  try {
    if (!cameraProcess) {
      return res.status(400).json({ message: "No camera process running" });
    }
    if (process.platform === "win32") {
      exec(`taskkill /pid ${cameraProcess.pid} /f /t`);
    } else {
      cameraProcess.kill();
    }
    cameraProcess = null;
    res.status(200).json({ message: "Camera stopped successfully" });
  } catch (error) {
    console.error("Error stopping camera:", error);
    res.status(500).json({ error: "Failed to stop camera" });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
