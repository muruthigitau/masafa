import React from "react";
import { motion } from "framer-motion";
import TableRow from "./TableRow";

const Table = ({
  columnsData,
  tableData,
  selectedRows,
  handleCellChange,
  handleDeleteRow,
  handleDuplicateRow,
  handleRowEdit,
  handleSelectAll,
  selectAll,
  readOnly,
  preview,
  getFieldDetails,
  ordered,
  configData,
  handleRowSelect,
}) => {
  const displayedTableData = tableData?.length > 0 ? tableData : [];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.1, ease: "easeInOut" }}
    >
      <table className="w-full table-condensed border border-gray-200 border-collapse text-xs text-center">
        <thead className="rounded-t-md bg-gray-200">
          <tr>
            <th className={`${readOnly ? "hidden" : ""}`}>
              <input
                type="checkbox"
                readOnly={readOnly}
                checked={selectAll}
                onChange={handleSelectAll}
                className="form-checkbox"
              />
            </th>
            <th></th>
            <th>ID</th>
            {columnsData.map((column) => (
              <th key={column.fieldname} className="px-2">
                {column.label}
              </th>
            ))}
            <th hidden={readOnly}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {displayedTableData.length === 0 && (
            <tr>
              <td
                colSpan={columnsData.length + 3}
                className="text-center py-4 text-gray-500 font-regular"
              >
                No data available
              </td>
            </tr>
          )}
          {displayedTableData.map((row, rowIndex) => (
            <TableRow
              key={rowIndex}
              rowIndex={rowIndex}
              row={row}
              columnsData={columnsData}
              selectedRows={selectedRows}
              handleCellChange={handleCellChange}
              handleDeleteRow={handleDeleteRow}
              handleDuplicateRow={handleDuplicateRow}
              handleRowEdit={handleRowEdit}
              readOnly={readOnly}
              preview={preview}
              getFieldDetails={getFieldDetails}
              configData={configData}
              handleRowSelect={handleRowSelect}
            />
          ))}
        </tbody>
      </table>
    </motion.div>
  );
};

export default Table;
