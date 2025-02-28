import React from "react";
import {
  FaUsers,
  FaFileInvoiceDollar,
  FaBox,
  FaShippingFast,
  FaMoneyBillWave,
  FaChartLine,
} from "react-icons/fa";

const ReportCards = ({ data, top_items }) => {
  if (!data) return <p className="text-gray-500 text-sm">No data available</p>;

  const cardData = [
    {
      title: "Customers",
      value: data.total_customers,
      icon: <FaUsers />,
      color: "bg-blue-100 text-blue-700",
    },
    {
      title: "Crossborders",
      value: data.total_crossborders,
      icon: <FaShippingFast />,
      color: "bg-green-100 text-green-700",
    },
    {
      title: "Items",
      value: data.total_items,
      icon: <FaBox />,
      color: "bg-yellow-100 text-yellow-700",
    },
    {
      title: "Invoices",
      value: data.total_invoices,
      icon: <FaFileInvoiceDollar />,
      color: "bg-purple-100 text-purple-700",
    },
    {
      title: "Payments",
      value: `KSH ${data.total_payments}`,
      icon: <FaMoneyBillWave />,
      color: "bg-red-100 text-red-700",
    },
    {
      title: "Avg Invoice Amount",
      value: `KSH ${data.avg_invoice_amount}`,
      icon: <FaChartLine />,
      color: "bg-indigo-100 text-indigo-700",
    },
  ];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-6 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6">
        {cardData.map((card, index) => (
          <div
            key={index}
            className={`p-4 rounded-lg shadow-md flex items-center ${card.color} hover:scale-105 transition-transform`}
          >
            <div className="text-2xl mr-4">{card.icon}</div>
            <div>
              <h3 className="text-sm font-medium text-gray-700">{card.title}</h3>
              <p className="text-lg font-semibold text-gray-900">{card.value}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Top Items with same styles as cards */}
      <div className="space-y-4">
        {top_items && top_items.length > 0 ? (
          <div className="grid grid-cols-2 gap-6 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6">
            {top_items.map((item, index) => (
              <div
                key={index}
                className={`p-4 rounded-lg shadow-md flex items-center bg-gray-100 text-gray-700 hover:scale-105 transition-transform`}
              >
                <div className="text-xl mr-4">{item.icon ? item.icon : <FaBox />}</div>
                <div>
                  <h3 className="text-sm font-medium">{item.name}</h3>
                  <p className="text-lg font-semibold">{item.count}</p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm text-gray-500">No top items available</p>
        )}
      </div>
    </div>
  );
};

export default ReportCards;
