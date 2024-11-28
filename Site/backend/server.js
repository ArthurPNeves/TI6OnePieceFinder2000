const express = require("express");
const cors = require("cors");
const multer = require("multer");
const fs = require("fs");
const path = require("path");

const app = express();
const PORT = 5000;

app.use(cors());

const upload = multer({ dest: "uploads/" });

app.post("/api/process", upload.single("image"), (req, res) => {
  if (!req.file) {
    return res.status(400).send("No file uploaded.");
  }

  console.log("File uploaded:", req.file);

  // Simulated processing (replace this with real logic)
  const processedFolderPath = path.join(__dirname, "processed");
  fs.readdir(processedFolderPath, (err, files) => {
    if (err) {
      console.error("Error reading processed folder:", err);
      return res.status(500).send("Server error.");
    }

    const processedImage = files.find((file) => /\.(jpg|jpeg|png)$/i.test(file));
    if (!processedImage) {
      return res.status(404).send("No processed image found.");
    }

    const processedImagePath = path.join(processedFolderPath, processedImage);
    res.sendFile(processedImagePath);
  });
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
