import React, { useState } from "react";
import WantedPoster from "./components/WantedPoster/WantedPoster.tsx";
import Handler from "./components/Handler/Handler.tsx";
import "./App.css";

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [processedImage, setProcessedImage] = useState(null); // State to store processed image URL

  const handleUploadClick = async () => {
    if (!selectedImage) {
      alert("Please select an image before uploading.");
      return;
    }

    const formData = new FormData();
    formData.append("image", selectedImage);

    try {
      const response = await fetch("http://localhost:5000/api/process", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const blob = await response.blob();
        const imageUrl = URL.createObjectURL(blob); // Convert the blob to a URL for display
        setProcessedImage(imageUrl); // Update the state with the received image
        alert("Image processed successfully!");
      } else {
        console.error("Error uploading image:", response.statusText);
      }
    } catch (err) {
      console.error("Error communicating with the backend:", err);
    }
  };

  return (
    <>
    <Handler />
    <div className='app-background'>
      <h1>Upload and Process Your Image</h1>
      <WantedPoster onImageSelect={setSelectedImage} />
      <button onClick={handleUploadClick}>Upload and Process</button>
      {processedImage && ( // Display the processed image below the button
        <div style={{ marginTop: "20px" }}>
          <h2>Processed Image:</h2>
          <img src={processedImage} alt="Processed" style={{ width: "300px", height: "auto" }}/>
        </div>
      )}
    </div>
    </>
  );
}

export default App;