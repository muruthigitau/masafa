import React, { useEffect, useState } from "react";
import {
  faBox,
  faFileInvoice,
  faMoneyBill,
  faUser,
  faTruck,
} from "@fortawesome/free-solid-svg-icons";
import LinkCard from "@/components/workspace/LinkCard";
import { FaChevronLeft, FaChevronRight } from "react-icons/fa";
import { fetchData } from "@/utils/Api";
import ReportCards from "./ReportCards";
import ReportGraph from "./Graph";

const links = [
  { href: `/app/item`, icon: faBox, text: "Items" },
  { href: `/app/invoice?type=Invoice`, icon: faFileInvoice, text: "Invoices" },
  { href: `/app/invoice?type=Quote`, icon: faTruck, text: "Quotes" },
  { href: `/app/payment`, icon: faMoneyBill, text: "Payments" },
  { href: `/app/customer`, icon: faUser, text: "Customers" },
  { href: `/app/crossborder`, icon: faTruck, text: "Crossborders" },
  { href: `/app/dispatch`, icon: faTruck, text: "Dispatches" },
  { href: `/app/driver`, icon: faTruck, text: "Drivers" },
  { href: `/app/vehicle`, icon: faTruck, text: "Vehicles" },
  { href: `/app/reminder`, icon: faTruck, text: "Reminders" },
];

const FILTER_OPTIONS = [
  { label: "Day", value: "day" },
  { label: "Week", value: "week" },
  { label: "Month", value: "month" },
  { label: "Year", value: "year" },
];

const AppDashboard = () => {
  const [reportData, setReportData] = useState(null);
  const [filter, setFilter] = useState("month");
  const [selectedDate, setSelectedDate] = useState("");

  useEffect(() => {
    const fetchReportData = async () => {
      try {
        const response = await fetchData(
          {},
          `reports/detailed?filter=${filter}${
            selectedDate ? `&date=${selectedDate}` : ""
          }`
        );

        setReportData({
          summary: {
            total_customers: response.data.total_customers,
            total_crossborders: response.data.total_crossborders,
            total_items: response.data.total_items,
            total_invoices: response.data.total_invoices,
            total_payments: response.data.total_payments,
            avg_invoice_amount: response.data.avg_invoice_amount,
          },
          analytics: response.data.analytics || [],
          top_items: response.data.top_items || [],
        });
      } catch (error) {
        console.error("Error fetching report data:", error);
      }
    };

    fetchReportData();
  }, [filter, selectedDate]);

  const adjustDate = (direction) => {
    const currentDate = selectedDate ? new Date(selectedDate) : new Date();

    switch (filter) {
      case "day":
        currentDate.setDate(
          currentDate.getDate() + (direction === "next" ? 1 : -1)
        );
        setSelectedDate(currentDate.toISOString().split("T")[0]);
        break;
      case "week":
        currentDate.setDate(
          currentDate.getDate() + (direction === "next" ? 7 : -7)
        );
        setSelectedDate(currentDate.toISOString().split("T")[0]);
        break;
      case "month":
        currentDate.setMonth(
          currentDate.getMonth() + (direction === "next" ? 1 : -1)
        );
        setSelectedDate(currentDate.toISOString().slice(0, 7));
        break;
      case "year":
        currentDate.setFullYear(
          currentDate.getFullYear() + (direction === "next" ? 1 : -1)
        );
        setSelectedDate(currentDate.getFullYear().toString());
        break;
      default:
        break;
    }
  };

  return (
    <div className="flex flex-col space-y-1 md:space-y-6 px-4 py-2 md:px-8 md:py-4 rounded-xl shadow-lg">
      <h2 className="text-2xl md:text-3xl font-bold text-purple-800">
        Dashboard
      </h2>
      {/* Navigation Links */}
      <div className="w-full">
        {/* <h2 className="text-lg md:text-xl font-semibold mb-4">Shortcuts</h2> */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
          {links.map((link, index) => (
            <LinkCard
              key={index}
              title={link.text}
              icon={link.icon}
              href={link.href}
              iconBg="bg-gradient-to-tl from-green-400 to-blue-500"
              tooltipContent={`Manage ${link.text}`}
              className="text-slate-800 text-base"
            />
          ))}
        </div>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-3 items-center py-4">
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {FILTER_OPTIONS.map((option) => (
            <button
              key={option.value}
              className={`px-3 py-1 w-full sm:w-28 h-12 text-sm md:text-md font-medium rounded-full transition-all duration-300 focus:outline-none shadow-md ${
                filter === option.value
                  ? "bg-purple-600 text-white"
                  : "bg-white text-purple-800 hover:bg-purple-200"
              }`}
              onClick={() => {
                setFilter(option.value);
                setSelectedDate("");
              }}
            >
              {option.label}
            </button>
          ))}
        </div>

        <div className="flex items-center space-x-3 bg-white px-2 py-2 md:px-4 md:py-2 rounded-full shadow-md">
          <button
            className="p-2 bg-purple-300 rounded-full hover:bg-purple-400"
            onClick={() => adjustDate("prev")}
          >
            <FaChevronLeft className="h-5 w-5 text-purple-800" />
          </button>
          <input
            type={
              filter === "day"
                ? "date"
                : filter === "week"
                ? "week"
                : filter === "month"
                ? "month"
                : filter === "year"
                ? "month"
                : "text"
            }
            min={filter === "year" ? "2000" : undefined}
            max={filter === "year" ? new Date().getFullYear() : undefined}
            className="px-2 py-2 w-full border border-purple-300 rounded-lg focus:ring focus:ring-purple-400 text-purple-800 bg-white"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
          />
          <button
            className="p-2 bg-purple-300 rounded-full hover:bg-purple-400"
            onClick={() => adjustDate("next")}
          >
            <FaChevronRight className="h-5 w-5 text-purple-800" />
          </button>
        </div>
      </div>

      {reportData ? (
        <>
          <ReportCards
            data={reportData?.summary}
            top_items={reportData?.top_items}
          />
          <ReportGraph data={reportData} />
        </>
      ) : (
        <p className="text-purple-600 text-md">Loading reports...</p>
      )}
    </div>
  );
};

export default AppDashboard;
