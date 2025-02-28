import React from "react";

const TextAreaField = ({
  value = "",
  onChange,
  readOnly,
  preview,
  hidden,
  handleInputChange,
  placeholder = "",
}) => {
  return (
    <div className="flex flex-col space-y-2 w-full">
      <textarea
        type="text"
        value={preview ? "" : value || ""} // In preview mode, do not display any value
        rows={8}
        readOnly={readOnly || preview} // Make input readOnly in both readOnly and preview mode
        disabled={readOnly || preview}
        onChange={handleInputChange || onChange}
        className="px-1 text-sm w-full focus:outline-none focus:ring-0 focus:border-none"
        placeholder={placeholder}
        hidden={hidden}
      />
    </div>
  );
};

export default TextAreaField;
