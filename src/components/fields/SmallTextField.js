import React from "react";

const SmallTextField = ({
  value = "",
  onChange,
  readOnly,
  preview,
  hidden,
  handleInputChange,
  placeholder = "Enter text",
}) => {
  return (
    <div className="flex flex-col space-y-2">
      <label className="text-sm font-semibold text-gray-700">Small Text</label>
      <textarea
        type="text"
        value={preview ? "" : value || ""} // In preview mode, do not display any value
        rows={8}
        readOnly={readOnly || preview} // Make input readOnly in both readOnly and preview mode
        disabled={readOnly || preview}
        hidden={hidden}
        className="px-1 text-sm w-full focus:outline-none focus:ring-0 focus:border-none"
        placeholder="Start typing your text here..."
      />
    </div>
  );
};

export default SmallTextField;
