import { useNavbar } from "@/contexts/NavbarContext";
import config from "@/modules/core/module.json";
import React, { useEffect } from "react";
import { useSidebar } from "@/contexts/SidebarContext";
import { ConfigProvider } from "@/contexts/ConfigContext";
import DoctypeForm from "@/components/pages/form";
import { useData } from "@/contexts/DataContext";
import { postData } from "@/utils/Api";

const NewModule = () => {
  const {
    updateDashboardText,
    updatePagesText,
    updateTextColor,
    updateIconColor,
  } = useNavbar();
  const { setSidebarHidden } = useSidebar();
  const { loading, setLoading } = useData();

  useEffect(() => {
    updateDashboardText("Documents");
    updatePagesText("Core");
    updateTextColor("text-white");
    updateIconColor("text-blue-200");
  }, []);

  const saveData = async (form) => {
    try {
      setLoading(true);

      const response = await postData(form, `modules`, true);

      if (
        response.data.additional &&
        response.data.additional.type === "newdoc"
      ) {
        const documentname = response.data.id;
        const app = response.data.app;
        const module = response.data.module;
        await addDoc({ documentname, app, module });
        router.push(`${router.pathname.replace("/new", "")}/${documentname}`);
      }
    } catch (error) {
      console.error("Error submitting form:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ConfigProvider initialConfig={config}>
      <DoctypeForm handleSave={saveData} config={config} is_doc={false} />
    </ConfigProvider>
  );
};

export default NewModule;
