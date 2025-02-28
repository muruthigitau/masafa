import { useEffect } from "react";
import { useNavbar } from "@/contexts/NavbarContext";
import { useSidebar } from "@/contexts/SidebarContext";
import NotFoundPage from "@/components/core/common/NotFound";

export default function Custom404() {
  const { updateDashboardText, updatePagesText, updateTextColor } = useNavbar();
  const { setSidebarHidden } = useSidebar();

  useEffect(() => {
    updateDashboardText("404");
    updatePagesText("Page Not Found");
    updateTextColor("text-slate-500");
    setSidebarHidden(true);
  }, []);

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gradient-to-r from-slate-500 via-blue-500 to-purple-500 text-white">
     <NotFoundPage />
    </div>
  );
}
