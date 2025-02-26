import React, { useState } from "react";

const ImageField = ({ value, onChange, readOnly, preview, hidden }) => {
  const [previewImage, setPreview] = useState(
    value ? URL.createObjectURL(value) : null
  );

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setPreview(URL.createObjectURL(file));
      onChange(file); // Pass the selected file back to the parent component
    }
  };

  const handleRemoveImage = () => {
    setPreview(null);
    onChange(null); // Clear the image in the parent component
  };

  return (
    <div className="image-field" hidden={hidden}>
      {previewImage ? (
        <div className="image-previewImage">
          <img
            src={previewImage}
            alt="Preview"
            className="image-preview__img"
          />
          <button
            type="button"
            className="image-preview__remove-btn"
            onClick={handleRemoveImage}
          >
            Remove Image
          </button>
        </div>
      ) : (
        <div className="image-upload">
          <label htmlFor="image-upload" className="image-upload__label">
            <span>Upload Image</span>
          </label>
          <input
            type="file"
            id="image-upload"
            accept="image/*"
            readOnly={readOnly || preview} // Make input readOnly in both readOnly and preview mode
            disabled={readOnly || preview}
            onChange={handleFileChange}
            className="image-upload__input"
          />
        </div>
      )}
    </div>
  );
};

export default ImageField;
