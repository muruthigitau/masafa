import React, { useRef } from "react";
import { useConfig } from "@/contexts/ConfigContext";
import FieldRenderer from "./FieldRenderer";
import { useData } from "@/contexts/DataContext";

const FieldItem = ({ item, handleFocus, placeholder = false }) => {
  const { selectedItem, setSelectedItem } = useConfig(); // Destructure setSelectedItem
  const { form, setForm, data } = useData();
  const ref = useRef(null);

  if (!item) {
    console.error(`Item is undefined`);
    return null;
  }

  const fieldValue = form && form[item?.fieldname] ? form[item?.fieldname] : null;

  const handleSelect = (e) => {
    e.stopPropagation();
    handleFocus(item);
  };

  const handleChange = (field, value) => {
    setForm((prevData) => ({
      ...prevData,
      [field.fieldname]: value,
    }));
  };

  return (
    <div
      ref={ref}
      className={`relative flex flex-col w-full break-words rounded-md font-bold text-[14px] px-2 text-gray-900 my-4 ${
        selectedItem === item ? "border-yellow-600" : "border-gray-300"
      } ${
        item?.read_only
          ? "text-gray-500"
          : item.fieldtype === "Check" ||
            item.fieldtype === "Button" ||
            item.fieldtype === "MultiSelect" ||
            item.fieldtype === "Table"
          ? "border-none bg-transparent py-2"
          : "border min-h-10 bg-white"
      } ${item?.hidden || (item?.read_only && !fieldValue) ? "hidden" : ""}`}
      onClick={handleSelect}
      tabIndex={0} // Allow the div to receive focus
    >
      <FieldRenderer
        fieldtype={item.fieldtype}
        item={item}
        value={fieldValue}
        placeholder={item?.label}
        handleInputChange={handleChange}
        label={item.label}
      />
    </div>
  );
};

export default FieldItem;
