import { useNavbar } from "@/contexts/NavbarContext";
import { appDetailConfig, newAppConfig } from "@/modules/core/apps";
import React, { useEffect } from "react";
import { useSidebar } from "@/contexts/SidebarContext";
import NewDoc from "@/components/pages/new/NewDoc";
import DocDetail from "@/components/pages/detail/DocDetail";

const AppDetail = () => {
  const {
    updateDashboardText,
    updatePagesText,
    updateTextColor,
    updateIconColor,
  } = useNavbar();
  const { setSidebarHidden } = useSidebar();

  useEffect(() => {
    updateDashboardText("Apps");
    updatePagesText("Core");
    updateTextColor("text-white");
    updateIconColor("text-blue-200");
    setSidebarHidden(false);
  }, []);
  return <DocDetail config={appDetailConfig} />;
};

export default AppDetail;
