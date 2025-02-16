import { useNavbar } from "@/contexts/NavbarContext";
import { useEffect } from "react";
import { useSidebar } from "@/contexts/SidebarContext";
import AppIndex from "@/templates/app";
import AppDashboard from "@/components/workspace/AppDashboard";

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
    updateTextColor("text-gray-900");
    updateIconColor("text-urple-800");
    setSidebarHidden(false);
  }, []);
  return (
    <div>
      <AppDashboard />
    </div>
  );
};

export default AppDetail;
