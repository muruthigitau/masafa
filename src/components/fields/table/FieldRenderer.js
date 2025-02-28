import React from "react";

import TextField from "@/components/fields/TextField";
import SelectField from "@/components/fields/SelectField";
import DateField from "@/components/fields/DateField";
import ButtonField from "@/components/fields/ButtonField";
import CheckField from "@/components/fields/CheckField";
import AttachField from "@/components/fields/AttachField";
import DataField from "@/components/fields/DataField";
import LinkField from "@/components/fields/LinkField";
import TableField from "@/components/fields/TableField";
import HtmlField from "@/components/fields/HtmlField";
import GeolocationField from "@/components/fields/GeolocationField";
import TextAreaField from "@/components/fields/TextAreaField";
import DatetimeField from "@/components/fields/DatetimeField";
import TimeField from "@/components/fields/TimeField";
import ColorField from "@/components/fields/ColorField"; // Assuming you have a ColorField component
import SignatureField from "@/components/fields/SignatureField"; // Assuming you have a SignatureField component
import JsonField from "../JsonField";
import ReadOnlyField from "../ReadOnlyField";

const FieldRenderer = ({
  fieldtype,
  item,
  value,
  handleInputChange,
  readOnly,
  label,
  minimal = false,
  // readOnly,
}) => {
  const fieldTypeMapping = {
    Text: { type: "text" },
    Data: { type: "text" },
    "Small Text": { type: "textarea" },
    "Long Text": { type: "textarea" },
    Password: { type: "password" },
    "HTML Editor": { type: "textarea" },
    "Markdown Editor": { type: "textarea" },
    "Text Editor": { type: "textarea" },
    Code: { type: "textarea" },
    Select: { type: "select" },
    Autocomplete: { type: "autocomplete" },
    "Table MultiSelect": { type: "multiselect" },
    Date: { type: "date" },
    Datetime: { type: "datetime-local" },
    Time: { type: "time" },
    Duration: { type: "duration" },
    Int: { type: "number" },
    Float: { type: "number" },
    Currency: { type: "number" },
    Percent: { type: "number" },
    Rating: { type: "rating" },
    Attach: { type: "file" },
    "Attach Image": { type: "image" },
    Check: { type: "checkbox" },
    Color: { type: "color" },
    Link: { type: "link" },
    "Dynamic Link": { type: "link" },
    Geolocation: { type: "geolocation" },
    Signature: { type: "signature" },
    "Read Only": { type: "text" },
    Button: { type: "button" },
    Barcode: { type: "barcode" },
    Icon: { type: "icon" },
    Heading: { type: "heading" },
    HTML: { type: "html" },
    Image: { type: "image" },
    JSON: { type: "json" },
    Table: { type: "table" },
    Phone: { type: "tel" }, // Added Phone as per the list
  };

  const fieldInfo = fieldTypeMapping[fieldtype] || {
    type: "unsupported",
  };
  const { type: generalType } = fieldInfo;

  switch (generalType) {
    case "text":
    case "number":
    case "password":
      return (
        <>
          <div className="text-right flex justify-between w-full">
            <TextField
              field={item}
              type={generalType}
              value={value}
              onChange={(e) => handleInputChange(item, e.target.value)}
              readOnly={readOnly}
            />
          </div>
        </>
      );
    case "textarea":
      return (
        <>
          <div className="text-right flex justify-between h-6 text-xs w-full">
            <TextAreaField
              field={item}
              value={value}
              onChange={(e) => handleInputChange(item, e.target.value)}
              rows={4}
              readOnly={readOnly}
            />
          </div>
        </>
      );
    case "select":
      return (
        <>
          <div className="text-right flex justify-between w-full">
            <SelectField
              field={item}
              value={value}
              onChange={(e) => handleInputChange(item, e)}
              options={item.options ? item.options.split("\n") : []}
              multiple={false}
              readOnly={readOnly}
            />
          </div>
        </>
      );
    case "autocomplete":
      return (
        <>
          <div className="text-right flex justify-between w-full">
            <SelectField
              field={item}
              value={value}
              onChange={(e) => handleInputChange(item, e)}
              options={item.options ? item.options.split("\n") : []}
              autocomplete={true}
              readOnly={readOnly}
            />
          </div>
        </>
      );
    case "multiselect":
      return (
        <>
          <div className="text-right flex justify-between w-full">
            <SelectField
              field={item}
              value={value}
              onChange={(items) => handleInputChange(item, items)}
              options={item.options ? item.options.split("\n") : []}
              multiple={true}
              readOnly={readOnly}
            />
          </div>
        </>
      );
    case "date":
      return (
        <>
          <div className="text-right flex justify-between w-full">
            <DateField
              field={item}
              value={value}
              onChange={(e) => {
                handleInputChange(item, e);
              }}
              readOnly={readOnly}
            />
          </div>
        </>
      );
    case "datetime-local":
      return (
        <>
          <div className="text-right flex justify-between w-full">
            <DatetimeField
              field={item}
              value={value}
              onChange={(e) => {
                handleInputChange(item, e);
              }}
              readOnly={readOnly}
            />
          </div>
        </>
      );
    case "time":
      return (
        <>
          <div className="text-right flex justify-between w-full">
            <TimeField
              field={item}
              value={value}
              onChange={(e) => {
                handleInputChange(item, e);
              }}
              readOnly={readOnly}
            />
          </div>
        </>
      );
    case "file":
    case "image":
      return (
        <>
          <div className="text-right flex justify-between w-full">
            <AttachField
              field={item}
              onChange={(e) => handleInputChange(item, e.target.files[0])}
              readOnly={readOnly}
            />
          </div>
        </>
      );
    case "checkbox":
      return (
        <div className="flex items-center -my-1">
          <CheckField
            field={item}
            checked={value}
            onChange={(e) => handleInputChange(item, e.target.checked)}
            readOnly={readOnly}
          />
          <span className="ml-2">{label}</span>
        </div>
      );
    case "button":
      return (
        <>
          <ButtonField
            field={item}
            label={item.label}
            onClick={() => handleInputChange(item, null)}
            readOnly={readOnly}
          />
        </>
      );
    case "readOnly":
      return (
        <>
          <div className="text-right flex justify-between w-full">
            <ReadOnlyField field={item} value={value} readOnly={readOnly} />
          </div>
        </>
      );
    case "link":
      return (
        <>
          <div className="text-right flex justify-between w-full">
            <LinkField
              field={item}
              value={value}
              onChange={(e) => handleInputChange(item, e)}
              readOnly={readOnly}
            />
          </div>
        </>
      );
    case "geolocation":
      return (
        <>
          <div className="text-right flex justify-between w-full">
            <GeolocationField
              field={item}
              value={value}
              onChange={(location) => handleInputChange(item, location)}
              readOnly={readOnly}
            />
          </div>
        </>
      );
    case "html":
      return (
        <>
          <div className="text-right flex justify-between w-full">
            <HtmlField
              field={item}
              value={value}
              onChange={(content) => handleInputChange(item, content)}
              readOnly={readOnly}
            />
          </div>
        </>
      );
    case "table":
      return (
        <>
          <TableField
            field={item}
            value={value}
            handleInputChange={(items) => handleInputChange(item, items)}
            options={item.options ? item.options.split("\n") : []}
            multiple={true}
            readOnly={readOnly}
          />
        </>
      );
    case "color":
      return (
        <>
          <div className="text-right flex justify-between w-full">
            <ColorField
              field={item}
              value={value}
              onChange={(color) => handleInputChange(item, color)}
              readOnly={readOnly}
            />
          </div>
        </>
      );
    case "signature":
      return (
        <>
          <div className="text-right flex justify-between w-full">
            <SignatureField
              field={item}
              value={value}
              onChange={(signature) => handleInputChange(item, signature)}
              readOnly={readOnly}
            />
          </div>
        </>
      );
    case "json":
      return (
        <>
          <div className="text-right flex justify-between w-full">
            <JsonField
              value={value}
              onChange={(json) => handleInputChange(item, json)}
              readOnly={readOnly}
            />
          </div>
        </>
      );
    case "unsupported":
    default:
      return (
        <>
          <div className="text-red-500">
            Unsupported field type: {fieldtype}
          </div>
        </>
      );
  }
};

export default FieldRenderer;
