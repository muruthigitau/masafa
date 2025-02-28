import { useNavbar } from "@/contexts/NavbarContext";
import { getFromDB } from "@/utils/indexedDB";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Link from "next/link";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import { v4 as uuidv4 } from 'uuid';

const SidebarList = ({ icon, text, link, permission }) => {
  const [isHovered, setIsHovered] = useState(false);
  const router = useRouter();
  const [perms, setPerms] = useState([]);

  const { dashboardText } = useNavbar();
  const active = dashboardText == text;

  // Generate a unique ID for each list item
  const uniqueId = uuidv4();

  useEffect(() => {
    const checkAuth = async () => {
      const perm = await getFromDB("permissions");
      setPerms(perm);
    };
    checkAuth();
  }, [router]);

  const handleMouseEnter = () => {
    setIsHovered(true);
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
  };

  // Check if permission is granted
  const hasPermission = () => {
    // If no specific permission is required, show the item
    if (!permission) {
      return true;
    }
    // If superuser or permissions contain "all", show the item
    if (perms === "all") {
      return true;
    }
    // Otherwise, check if the specific permission exists in the permissions array
    return perms?.includes(permission);
  };

  // Only render the `li` if the user has permission
  if (!hasPermission()) {
    return null; // Don't render the `li` if the user lacks permission
  }

  return (
    <li id={uniqueId} key={uniqueId} className="mt-0.5 w-full">
      <Link
        href={link}
        className={`py-2 text-sm ease-nav-brand my-0 mx-2 flex items-center whitespace-nowrap rounded-lg px-2 font-semibold text-slate-700 transition-colors ${
          isHovered || active ? "shadow-soft-xl bg-white" : ""
        }`}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
      >
        <div
          className={`mr-2 flex h-8 w-8 items-center justify-center rounded-lg bg-center stroke-0 text-center xl:p-2.5 ${
            isHovered || active
              ? "shadow-soft-xl bg-gradient-to-tl from-purple-700 to-pink-500 text-white"
              : "shadow-soft-2xl"
          }`}
        >
          <FontAwesomeIcon
            icon={icon}
            style={{ color: isHovered || active ? "#FFFFFF" : "#701a75" }}
          />
        </div>
        <span className="ml-1 duration-300 opacity-100 pointer-events-none ease-soft">
          {text}
        </span>
      </Link>
    </li>
  );
};

export default SidebarList;
