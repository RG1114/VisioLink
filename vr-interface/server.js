const express = require("express");
const os = require("os");
const { exec } = require("child_process");

const app = express();
const PORT = 5000;

function getServerIP() {
    const interfaces = os.networkInterfaces();
    for (let interfaceName in interfaces) {
        for (let iface of interfaces[interfaceName]) {
            if (iface.family === "IPv4" && !iface.internal) {
                return iface.address;
            }
        }
    }
    return "Not Available";
}

app.get("/get-ip", (req, res) => {
    res.json({ ip: getServerIP() });
});

app.get("/start-camera", (req, res) => {
    exec("python run_gesture_model.py", (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return res.status(500).send("Failed to start camera.");
        }
        res.send("Camera started successfully.");
    });
});

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
