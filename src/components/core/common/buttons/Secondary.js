import React from "react";

const SecondaryButton = ({ text, className, onClick }) => {
  return (
    <div
      onClick={onClick}
      className={`inline-block px-2 py-1 mb-0 font-bold text-center uppercase align-middle transition-all border border-solid rounded-lg shadow-none cursor-pointer leading-pro ease-soft-in text-xs bg-150 active:opacity-85 hover:scale-102 tracking-tight-soft bg-x-25 bg-fuchsia-500 text-white hover:opacity-75 ${className}`}
    >
      {text}
    </div>
  );
};

export default SecondaryButton;
