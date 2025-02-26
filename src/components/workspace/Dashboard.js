import React, { useState, useEffect } from "react";
import {
  faBook,
  faBookOpen,
  faBookReader,
  faBox,
  faPlus,
} from "@fortawesome/free-solid-svg-icons";
import LinkSection from "@/components/workspace/LinkSection";
import LinkCard from "@/components/workspace/LinkCard";

import config from "@/data/config.json";

const Dashboard = () => {
  const [appModules, setAppModules] = useState([]);

  useEffect(() => {
    setAppModules(config);
  }, []);

  return (
    <div className="flex flex-col">
    

      <div className="w-full px-3 mt-6">
        <h6 className="pl-3 ml-2 text-sm font-bold leading-tight text-pink-900 uppercase opacity-90">
          Actions
        </h6>
        <div className="grid grid-cols-2 md:grid-cols-4 px-4 py-2 gap-4">
          <LinkCard
            title="Apps"
            icon={faBook}
            href="/apps"
            iconBg="bg-gradient-to-tl from-blue-400 to-green-500"
            bgColor="bg-white"
            tooltipContent="App list"
          />
          <LinkCard
            title="Modules"
            icon={faBookOpen}
            href="/modules"
            iconBg="bg-gradient-to-tl from-blue-400 to-green-500"
            bgColor="bg-white"
            tooltipContent="Manage modules"
          />
          <LinkCard
            title="Documents"
            icon={faBookReader}
            href="/documents"
            iconBg="bg-gradient-to-tl from-blue-400 to-green-500"
            bgColor="bg-white"
            tooltipContent="Manage documents"
          />
        </div>
        <h6 className="pl-3 ml-2 text-sm mt-4 font-bold leading-tight uppercase opacity-60">
          Module List
        </h6>
        <div className="grid grid-cols-2 md:grid-cols-4 px-4 py-2 gap-4">
          {Object.keys(appModules).map((appName, index) => (
            <LinkCard
              key={index}
              title={`${appName.charAt(0).toUpperCase() + appName.slice(1)}`}
              icon={faBox}
              href={`/${appName}`}
              iconBg="bg-gradient-to-tl from-green-400 to-blue-500"
              bgColor="bg-white"
              tooltipContent={`Manage ${appName}`}
            />
          ))}
        </div>
      </div>

      <div className="px-6 grid grid-cols-1 md:grid-cols-2 gap-4">
        {Object.keys(appModules).map((appName) => (
          <LinkSection
            key={appName}
            title={`${
              appName.charAt(0).toUpperCase() + appName.slice(1)
            } Modules`}
            description={`Manage modules for ${
              appName.charAt(0).toUpperCase() + appName.slice(1)
            }.`}
            tooltipContent={`Manage modules for ${
              appName.charAt(0).toUpperCase() + appName.slice(1)
            }.`}
            links={appModules[appName].modules.map((module) => ({
              href: `/${appName}/${module.moduleName}`,
              text: `${
                module.moduleName.charAt(0).toUpperCase() +
                module.moduleName.slice(1)
              }`,
              icon: faBox,
            }))}
            bgColor="bg-gradient-to-tl from-blue-200 to-green-200"
            textColor="text-gray-900"
          />
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
