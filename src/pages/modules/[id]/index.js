import { useNavbar } from "@/contexts/NavbarContext";
import config from "@/modules/core/module.json";
import React, { useEffect, useState } from "react";
import { useSidebar } from "@/contexts/SidebarContext";
import { ConfigProvider } from "@/contexts/ConfigContext";
import DoctypeForm from "@/components/pages/form";
import { useData } from "@/contexts/DataContext";
import { fetchData, postData, updateData } from "@/utils/Api";
import { useRouter } from "next/router";

const ModuleDetail = () => {
  const {
    updateDashboardText,
    updatePagesText,
    updateTextColor,
    updateIconColor,
  } = useNavbar();
  const { setSidebarHidden } = useSidebar();
  const { loading, setLoading, setData, setForm } = useData();
  const [appData, setAppData] = useState(null);
  const router = useRouter();
  const { id } = router.query;

  useEffect(() => {
    const fetchDataAsync = async () => {
      updateDashboardText("Documents");
      updatePagesText("Core");
      updateTextColor("text-white");
      updateIconColor("text-blue-200");
      const responseData = await fetchData({}, `modules/${id}`);
      if (responseData?.data) {
        setAppData({
          app: responseData.data.app,
          module: id,
          enpoint: `modules/${id}`,
        });
        setData(responseData.data);
        setForm(responseData.data);
      }
    };
    fetchDataAsync();
  }, [id]);

  const saveData = async (form) => {
    try {
      setLoading(true);

      const response = await updateData(form, `modules/${id}`, true);
    } catch (error) {
      console.error("Error submitting form:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ConfigProvider initialConfig={config} initialAppData={appData}>
      <DoctypeForm handleSave={saveData} config={config} is_doc={false} />
    </ConfigProvider>
  );
};

export default ModuleDetail;
