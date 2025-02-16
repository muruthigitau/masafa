import React, { Suspense, useEffect, useRef, useState } from "react";
import clsx from "clsx";
import { useConfig } from "@/contexts/ConfigContext";
import FieldItem from "../FieldItem";

const ColumnItem = ({ section, column, handleFocus, handleBlur }) => {
  // Dragging logic for the column (already in place)
  const { selectedItem, localConfig, selectedTab, setLocalConfig } =
    useConfig();

  return (
    <Suspense fallback={<div>Loading...</div>}>
      <div className={clsx("flex-1 rounded-md")}>
        {column?.label && (
          <div className="flex flex-row w-full h-fit justify-between">
            <h5 className="text-md font-semibold p-2">{column.label}</h5>
          </div>
        )}

        {/* Render draggable items inside the column */}
        {column?.fields?.map((item) => (
          <Suspense fallback={<div>Loading...</div>} key={item.fieldname}>
            <FieldItem
              item={item}
              handleFocus={handleFocus}
              handleBlur={handleBlur}
            />
          </Suspense>
        ))}
      </div>
    </Suspense>
  );
};

export default ColumnItem;
