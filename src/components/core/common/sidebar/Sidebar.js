import React, { useRef, useEffect, useState } from "react";
import Documentation from "@/components/core/common/sidebar/Documentation";
import SidebarList from "@/components/core/common/sidebar/List";
import {
  faDashboard,
  faUser,
  faAngleDoubleLeft,
  faAngleDoubleRight,
  faUserFriends,
  faCogs,
  faDiagnoses,
  faBook,
  faTools,
  faBars,
  faFileInvoice,
  faBox,
  faChartBar,
  faTruckPickup,
  faTruckLoading,
  faDriversLicense,
  faCar,
  faCartShopping,
  faPerson,
  faQuoteLeft,
  faMoneyBillTransfer,
  faBell,
  faSailboat,
  faUserCheck,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useSidebar } from "@/contexts/SidebarContext";
import { useNavbar } from "@/contexts/NavbarContext";
import { useRouter } from "next/router";
import sidebarConfig from "@/data/sidebar.json"; // Import sidebar.json for sidebar settings
import { generateSidebarData } from "../../../../utils/generateSidebarData";

const Sidebar = () => {
  const { sidebarWidth, setSidebarWidth, sidebarHidden } = useSidebar();
  const { dashboardText } = useNavbar();
  const sidebarRef = useRef(null);
  const [isCollapsed, setIsCollapsed] = useState(false);
  const router = useRouter();

  const { apps, modules, developerMode } = generateSidebarData();

  // Extract sidebar links from sidebarConfig
  const sidebarLinks = sidebarConfig.sidebarLinks || []; // Assuming the sidebar.json has a links array

  useEffect(() => {
    const handleResize = () => {
      if (sidebarHidden) {
        setIsCollapsed(true);
      } else {
        if (sidebarRef.current) {
          setIsCollapsed(window.innerWidth < 1150);
        }
      }
    };

    handleResize();

    window.addEventListener("resize", handleResize);
    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, [router, sidebarHidden]);

  useEffect(() => {
    if (sidebarRef.current) {
      setSidebarWidth(sidebarRef.current.offsetWidth);
    }
  }, [isCollapsed, sidebarHidden]);

  const toggleSidebar = () => {
    setIsCollapsed(!isCollapsed);
  };

  return (
    <>
      {!isCollapsed && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm z-50 md:hidden"
          onClick={toggleSidebar}
        ></div>
      )}
      <aside
        className={`${
          !sidebarHidden ? "" : "hidden"
        } -mt-16 md:mt-0 w-fit relative z-100 md:z-0 flex flex-col`}
        ref={sidebarRef}
      >
        {isCollapsed && (
          <button
            onClick={toggleSidebar}
            className="w-fit fixed z-100 text-slate-700 py-2 px-2 group text-sm md:text-xl top-2 md:top-16 bg-gray-50 rounded" // Use group class for managing hover effect
          >
            {/* Default icon (faBars) */}
            <FontAwesomeIcon
              icon={faBars}
              className="transition-all duration-300 ease-in-out group-hover:hidden" // Hide on hover
            />
            {/* Hover icon (faAngleDoubleRight) */}
            <FontAwesomeIcon
              icon={faAngleDoubleLeft}
              className="transition-all duration-300 ease-in-out hidden group-hover:block" // Show on hover
            />
          </button>
        )}

        <div
          className={`w-fit pb-8 max-h-[calc(100vh+64px)] md:max-h-[92vh] overflow-auto ease-nav-brand block -translate-x-full flex-wrap flex-grow items-center justify-between border-0 p-1 antialiased transition-transform duration-200 left-0 translate-x-0 ${
            !isCollapsed ? "fixed md:relative pt-6 md:pt-0 bg-white" : "hidden"
          }`}
        >
          <div className="h-fit flex items-center justify-between px-4">
            <button
              onClick={toggleSidebar}
              className="group text-sm md:text-xl flex py-2" // Use group class for managing hover effect
            >
              {/* Default icon (faBars) */}
              <FontAwesomeIcon
                icon={faBars}
                className="transition-all duration-300 ease-in-out group-hover:hidden" // Hide on hover
              />
              {/* Hover icon (faAngleDoubleRight) */}
              <FontAwesomeIcon
                icon={faAngleDoubleRight}
                className="transition-all duration-300 ease-in-out hidden group-hover:block" // Show on hover
              />
            </button>
            <a
              className="block py-2 m-0 text-sm flex flex-col whitespace-nowrap justify-center items-center text-slate-700"
              target="_blank"
              rel="noreferrer"
              href="/"
            >
              <span className="ml-4 mr-2 font-semibold text-xl transition-all duration-200 ease-nav-brand">
                {dashboardText}
              </span>
            </a>
          </div>

          <hr className="h-px mt-0 bg-transparent bg-gradient-to-r from-transparent via-black/40 to-transparent" />

          <div className="items-center block w-auto h-fit grow basis-full scrollbar scrollbar-thin scrollbar-thumb-slate-50 scrollbar-track-slate-100 pr-2">
            <ul className="flex flex-col mb-4">
              <SidebarList
                icon={faDashboard}
                text="Home"
                link="/"
                active={dashboardText === ("Home" || "Dashboard" || "")}
              />
              <SidebarList
                icon={faCartShopping}
                text="Item"
                link="/app/item"
                permission="view_item"
                active={dashboardText === "Item"}
              />
              <SidebarList
                icon={faTruckLoading}
                text="Crossborder"
                link="/app/crossborder"
                permission="view_crossborder"
                active={dashboardText === "Crossborder"}
              />
              <SidebarList
                icon={faPerson}
                text="Customer"
                link="/app/customer"
                permission="view_customer"
                active={dashboardText === "Customer"}
              />
              <SidebarList
                icon={faSailboat}
                text="Supplier"
                link="/app/supplier"
                permission="view_supplier"
                active={dashboardText === "Supplier"}
              />
              <SidebarList
                icon={faFileInvoice}
                text="Invoice"
                link="/app/invoice?type=Invoice"
                permission="view_invoice"
                active={dashboardText === "Invoice"}
              />
              <SidebarList
                icon={faFileInvoice}
                text="Add Invoice"
                link="/app/invoice/new"
                permission="view_invoice"
                active={dashboardText === "Add Invoice"}
              />

              <SidebarList
                icon={faQuoteLeft}
                text="Quote"
                link="/app/invoice?type=Quote"
                permission="view_invoice"
                active={dashboardText === "Quote"}
              />
              <SidebarList
                icon={faMoneyBillTransfer}
                text="Payment"
                link="/app/payment"
                permission="view_payment"
                active={dashboardText === "Payment"}
              />
              <SidebarList
                icon={faMoneyBillTransfer}
                text="Paymentdetails"
                link="/app/paymentdetails"
                permission="view_paymentdetails"
                active={dashboardText === "Paymentdetails"}
              />
              <SidebarList
                icon={faTruckPickup}
                text="Dispatch"
                link="/app/dispatch"
                permission="view_dispatch"
                active={dashboardText === "Dispatch"}
              />
              <SidebarList
                icon={faDriversLicense}
                text="Driver"
                link="/app/driver"
                permission="view_driver"
                active={dashboardText === "Driver"}
              />
              <SidebarList
                icon={faUserCheck}
                text="Employee"
                link="/app/employee"
                permission="view_employee"
                active={dashboardText === "Employee"}
              />
              <SidebarList
                icon={faCar}
                text="Vehicle"
                link="/app/vehicle"
                permission="view_vehicle"
                active={dashboardText === "Vehicle"}
              />
              <SidebarList
                icon={faBell}
                text="Reminder"
                link="/app/reminder"
                permission="view_reminder"
                active={dashboardText === "Reminder"}
              />

              {/* Dynamically add links from sidebar.json */}
              {sidebarLinks.map((link) => (
                <SidebarList
                  key={link.text} // Use text as key or any unique identifier
                  icon={link.icon} // Adjust the icon or load dynamically from sidebar.json
                  text={link?.text}
                  link={link?.link}
                />
              ))}
              {developerMode && (
                <>
                  {/* New Section for Apps */}
                  <li className="w-full mb-2 mt-6 pr-2">
                    <h6 className="pl-3 ml-2 text-xs font-bold leading-tight uppercase opacity-60">
                      Apps
                    </h6>
                  </li>
                  {apps.map((app) => (
                    <SidebarList
                      key={app.id}
                      icon={faBook} // Replace with a suitable icon if needed
                      text={app.name} // Capitalize the app name
                      link={app.link} // Link to /appname
                    />
                  ))}

                  {/* New Section for Modules */}
                  {/* <li className="w-full my-2 pr-2">
                    <h6 className="pl-3 ml-2 text-xs font-bold leading-tight uppercase opacity-60">
                      Modules
                    </h6>
                  </li> */}
                </>
              )}
              {/* 
              {modules.map((module) => (
                <SidebarList
                  key={module.id} // Unique key for each module
                  icon={faBookOpen} // Replace with a suitable icon if needed
                  text={module.name} // Capitalize the module name
                  link={module?.link} // Link to /appname/modulename
                />
              ))} */}

              <li className="w-full mb-2 mt-6 pr-2">
                <h6 className="pl-3 ml-2 text-xs font-bold leading-tight uppercase opacity-60">
                  Admin
                </h6>
              </li>
              <SidebarList
                icon={faUser}
                text="Profile"
                link="/profile"
                active={dashboardText === "Profile"}
              />
              <SidebarList
                icon={faUserFriends}
                text="Users"
                link="/app/user"
                permission="view_user"
                active={dashboardText === "User"}
              />
              <SidebarList
                icon={faCogs}
                text="Rolegroup"
                link="/app/group"
                permission="view_rolegroup"
                active={dashboardText === "Group"}
              />
              <SidebarList
                icon={faDiagnoses}
                text="Permissions"
                link="/app/permission"
                permission="view_permission"
                active={dashboardText === "Permission"}
              />

              {developerMode && (
                <>
                  <li className="w-full my-2 pr-2">
                    <h6 className="pl-3 ml-2 text-xs font-bold leading-tight uppercase opacity-60">
                      Developer Settings
                    </h6>
                  </li>
                  <SidebarList
                    icon={faTools}
                    text="Settings"
                    link="/settings"
                    active={dashboardText === "Settings"}
                  />
                </>
              )}

              <Documentation />
            </ul>
          </div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
