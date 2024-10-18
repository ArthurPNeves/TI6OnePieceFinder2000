import React, { useState } from "react";
import UploadButton from "./UploadButton.tsx";

const WantedPoster: React.FC = () => {
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);

  const mainContainerStyle: React.CSSProperties = {
    display: "flex", 
    justifyContent: "center", 
    alignItems: "flex-start",
    backgroundColor: '#EBCE9C',
    padding: "20px",
    marginTop: "100px"
  };

  const imageStyle: React.CSSProperties = {
    width: "300px", 
    height: "auto",
    marginRight: "100px",
    marginTop: "60px"
  };

  const posterContainerStyle: React.CSSProperties = {
    position: "relative",
    display: "inline-block",
    width: "400px",
    height: "auto",
  };

  const posterStyle: React.CSSProperties = {
    display: "block",
    width: "100%",
    height: "auto", 
    zIndex: 2,
    position: "relative",
  };

  const uploadedImageStyle: React.CSSProperties = {
    position: "absolute",
    top: "10%",
    left: "10%",
    width: "80%",
    height: "auto",
    zIndex: 1,
    marginTop: "74px"
  };

  const handleImageUpload = (file: File) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      if (e.target?.result) {
        setUploadedImage(e.target.result as string);
      }
    };
    reader.readAsDataURL(file); 
  };

  return (
    <div style={mainContainerStyle}>
      <img src="./img/luf-Photoroom.png" alt="Luffy Wanted Poster" style={imageStyle} />

      <div style={posterContainerStyle}>
        {uploadedImage && (
          <img src={uploadedImage} alt="Uploaded" style={uploadedImageStyle} />
        )}

        <img src="/img/cartazF.png" alt="Wanted Poster" style={posterStyle} />

        {!uploadedImage && <UploadButton onImageUpload={handleImageUpload} />}
      </div>
    </div>
  );
};

export default WantedPoster;
