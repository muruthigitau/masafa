import React from "react";

const HtmlField = ({ html, value, onChange, readOnly, preview, hidden }) => (
  <div
    dangerouslySetInnerHTML={{ __html: html }}
    className="px-1 text-sm w-full focus:outline-none focus:ring-0 focus:border-none"
    readOnly={readOnly || preview} // Make input readOnly in both readOnly and preview mode
    disabled={readOnly || preview}
    hidden={hidden}
  />
);

export default HtmlField;
