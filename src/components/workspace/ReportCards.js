import React from "react";
import {
  FaUsers,
  FaFileInvoiceDollar,
  FaBox,
  FaShippingFast,
  FaMoneyBillWave,
  FaChartLine,
} from "react-icons/fa";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

const ReportCards = ({ data }) => {
  if (!data) return <p className="text-gray-500 text-sm">No data available</p>;

  const cardData = [
    {
      title: "Customers",
      value: data.total_customers,
      icon: <FaUsers />,
      color: "bg-blue-50 text-blue-700",
    },
    {
      title: "Crossborders",
      value: data.total_crossborders,
      icon: <FaShippingFast />,
      color: "bg-green-50 text-green-700",
    },
    {
      title: "Items",
      value: data.total_items,
      icon: <FaBox />,
      color: "bg-yellow-50 text-yellow-700",
    },
    {
      title: "Invoices",
      value: data.total_invoices,
      icon: <FaFileInvoiceDollar />,
      color: "bg-purple-50 text-purple-700",
    },
    {
      title: "Payments",
      value: `KSH ${data.total_payments}`,
      icon: <FaMoneyBillWave />,
      color: "bg-red-50 text-red-700",
    },
    {
      title: "Avg Invoice Amount",
      value: `KSH ${data.avg_invoice_amount}`,
      icon: <FaChartLine />,
      color: "bg-indigo-50 text-indigo-700",
    },
  ];

  return (
    <div className="grid grid-cols-2 gap-4 md:grid-cols-4 lg:grid-cols-6">
      {cardData.map((card, index) => (
        <div
          key={index}
          className={`p-3 rounded-md shadow-sm flex items-center ${card.color}`}
        >
          <div className="text-lg mr-3">{card.icon}</div>
          <div>
            <h3 className="text-xs font-medium">{card.title}</h3>
            <p className="text-sm font-semibold">{card.value}</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ReportCards;
