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

const ReportGraph = ({ data }) => {
  if (!data || !data.analytics)
    return <p className="text-gray-500 text-sm">No data available</p>;

  const formattedData = data.analytics.map((entry) => ({
    month: new Date(entry.period).toLocaleString("default", {
      month: "short",
      year: "2-digit",
    }),
    invoices: entry.total_invoices,
    payments: entry.total_invoice_amount,
    items: entry.total_items,
  }));

  return (
    <div className="bg-white p-4 shadow rounded-md">
      <h2 className="text-sm font-medium text-gray-700 mb-2">Monthly Report</h2>
      <ResponsiveContainer width="100%" height={160}>
        <BarChart
          data={formattedData}
          margin={{ top: 5, right: 10, left: -10, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
          <XAxis dataKey="month" tick={{ fontSize: 10, fill: "#6B7280" }} />
          <YAxis tick={{ fontSize: 10, fill: "#6B7280" }} />
          <Tooltip />
          <Bar
            dataKey="invoices"
            fill="#4CAF50"
            radius={[2, 2, 0, 0]}
            barSize={22}
          />
          <Bar
            dataKey="payments"
            fill="#34D399"
            radius={[2, 2, 0, 0]}
            barSize={22}
          />
          <Bar
            dataKey="items"
            fill="#FFA500"
            radius={[2, 2, 0, 0]}
            barSize={22}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ReportGraph;
