import { arrangeFieldsIntoSectionsAndColumns } from "./arrangeFieldsBySectionsAndColumns";

export const getFieldsForTab = (config, tabBreak = null) => {
  if (!config?.fields || !config?.field_order) {
    return arrangeFieldsIntoSectionsAndColumns([]);
  }
  let tabFieldList = [];
  // Helper function to find a field by fieldname
  const findField = (fieldname) =>
    config.fields.find((field) => field.fieldname === fieldname);

  // If no specific tabBreak?.fieldname is passed, return all fields in the order of field_order
  if (!tabBreak?.fieldname) {
    tabFieldList = config.field_order
      .map((fieldname) => findField(fieldname))
      .filter(Boolean);
  }

  if (tabBreak?.odd) {
    const firstTabIndex = config.field_order.findIndex(
      (fieldname) => findField(fieldname)?.fieldtype === "Tab Break"
    );

    // If there are no "Tab Breaks", tabFieldList = all fields
    if (firstTabIndex === -1) {
      tabFieldList = config.field_order
        .map((fieldname) => findField(fieldname))
        .filter(Boolean);
      return arrangeFieldsIntoSectionsAndColumns(tabFieldList);
    }

    // tabFieldList = all fields before the first "Tab Break"
    tabFieldList = config.field_order
      .slice(0, firstTabIndex)
      .map((fieldname) => findField(fieldname))
      .filter(Boolean);

    return arrangeFieldsIntoSectionsAndColumns(tabFieldList); // Passing tabBreak here
  }

  // Handle a specific tabBreak?.fieldname
  const startIndex = config.field_order.findIndex(
    (fieldname) => fieldname === tabBreak?.fieldname
  );

  // If the tabBreak?.fieldname is not found, return an empty array
  if (startIndex === -1) {
    return [];
  }

  const endIndex = config.field_order.findIndex(
    (fieldname, idx) =>
      idx > startIndex && findField(fieldname)?.fieldtype === "Tab Break"
  );

  // Use the last index if no Tab Break is found
  const adjustedEndIndex =
    endIndex === -1 ? config.field_order.length : endIndex;

  // Return all fields between the current tabBreak?.fieldname and the next one
  tabFieldList = config.field_order
    .slice(startIndex + 1, adjustedEndIndex)
    .map((fieldname) => findField(fieldname))
    .filter(Boolean);

  return arrangeFieldsIntoSectionsAndColumns(tabFieldList, tabBreak); // Passing tabBreak here
};
