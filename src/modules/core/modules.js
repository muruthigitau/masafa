import {
  faBox,
  faInfoCircle,
  faNewspaper,
  faStoreSlash,
} from "@fortawesome/free-solid-svg-icons";

const commonFields = [
  {
    name: "ID",
    type: "text",
    id: "id",
    icon: faBox,
    bgColor: "green",
  },
  {
    name: "App",
    type: "linkselect",
    id: "app",
    endpoint: "apps",
    icon: faBox,
    bgColor: "green",
  },
  {
    name: "Status",
    type: "select",
    id: "status",
    icon: faStoreSlash,
    options: [
      {
        label: "Active",
        value: "Active",
        style: "from-green-600 to-lime-400",
      },
      {
        label: "Disabled",
        value: "Disabled",
        style: "from-slate-600 to-slate-300",
      },
    ],
  },
  { name: "Name", type: "text", id: "name", icon: faNewspaper },
  {
    name: "Description",
    type: "textarea",
    id: "description",
    required: false,
    icon: faInfoCircle,
  },
];

// Filters for ListTable
export const moduleFilters = {
  status: {
    type: "select",
    options: [
      { value: "", label: "All" },
      { value: "Active", label: "Active" },
      { value: "Disabled", label: "Disabled" },
    ],
  },
  name: {
    type: "text",
  },
  app: {
    type: "text",
  },
  id: {
    type: "text",
  },
};

// Configurations for DocDetail
export const moduleDetailConfig = {
  endpoint: "modules",
  fields: commonFields.filter((field) => field.name !== "ID"),
};

// Configurations for ListTable
export const moduleListConfig = {
  name: "modules",
  fields: commonFields,
  data: [],
};

// Configurations for NewDoc
export const newModuleConfig = {
  endpoint: "modules",
  name: "module",
  fields: commonFields.filter((field) => field.name !== "ID"),
  data: [],
};
