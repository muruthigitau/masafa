export default class CustomElements {
  constructor(form, setForm, data, setData, router, reloadData, setLoading) {
    this.form = form;
    this.setForm = setForm;
    this.data = data;
    this.setData = setData;
    this.router = router;
    this.reloadData = reloadData;
    this.setLoading = setLoading;
  }

  // Lifecycle hooks
  lifecycleHooks = {
    beforeSave: (form) => {
      console.log("Before Save Hook Executed", form);
      // return cleanData(form);
    },
    afterSave: (form) => {
      console.log("After Save Hook Executed");
    },
    onFieldChange: (field, value) => {
      console.log(`Field Changed: ${field} => ${value}`);
      this.setForm((prev) => ({ ...prev, [field]: value }));
    },
  };

  // Custom Buttons
  customButtons = [
    {
      label: "Custom Action",
      type: "primary",
      text: "⚡",
      action: () => console.log("Custom Action Executed"),
    },
    {
      label: "Refresh",
      text: "🔄",
      action: () => this.reloadData(this.router),
    },
  ];

  // Custom Components
  customComponents = [
    ({ form }) => (
      <div className="bg-blue-100 p-2 rounded-md">
        <p>Custom Component Loaded</p>
        <p>Form Data: {JSON.stringify(form, null, 2)}</p>
      </div>
    ),
  ];
}
