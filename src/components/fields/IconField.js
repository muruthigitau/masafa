import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

const IconField = ({ icon, value, onChange, readOnly, preview, hidden }) => (
  <div
    onClick={onChange}
    readOnly={readOnly || preview} // Make input readOnly in both readOnly and preview mode
    disabled={readOnly || preview}
    hidden={hidden}
  >
    <FontAwesomeIcon icon={icon} className="text-xs" />
  </div>
);

export default IconField;
