import React from "react";

const Pagination = ({
  currentPage,
  totalPages,
  onPageChange,
  itemsPerPage,
  onItemsPerPageChange,
  total_entries,
}) => {
  if (!totalPages) {
    return;
  }
  let pagination_data = [];
  if (totalPages <= 15) {
    for (let i = 1; i <= totalPages; i++) {
      pagination_data.push(i);
    }
  } else {
    for (let i = 1; i <= 5; i++) {
      pagination_data.push(i);
    }
    if (currentPage < 10) {
      for (let i = 6; i <= 10; i++) {
        pagination_data.push(i);
      }
      pagination_data.push("...");
      for (let i = totalPages - 4; i <= totalPages; i++) {
        pagination_data.push(i);
      }
    } else if (currentPage > totalPages - 10) {
      pagination_data.push("...");
      for (let i = totalPages - 9; i <= totalPages; i++) {
        pagination_data.push(i);
      }
    } else {
      pagination_data.push("...");
      for (let i = currentPage - 2; i <= currentPage + 2; i++) {
        pagination_data.push(i);
      }
      pagination_data.push("...");
      for (let i = totalPages - 4; i <= totalPages; i++) {
        pagination_data.push(i);
      }
    }
  }

  const renderPageNumbers = () => {
    return pagination_data?.map((page, index) => {
      if (page === "...") {
        return (
          <li key={index}>
            <span className="relative flex items-center justify-center font-medium min-w-[2rem] px-1 py-2 rounded-md outline-none cursor-default">
              {page}
            </span>
          </li>
        );
      }
      return (
        <li key={index}>
          <button
            type="button"
            onClick={() => onPageChange(page)}
            className={`relative flex items-center justify-center font-medium min-w-[2rem] px-1 py-1 mx-1 rounded-md outline-none transition ${
              currentPage === page
                ? "text-purple-900 bg-purple-500/10 ring-1 ring-purple-500"
                : "hover:bg-gray-500/5 bg-white focus:bg-purple-500/10 dark:hover:bg-gray-400/5 focus:text-purple-900"
            }`}
          >
            <span>{page}</span>
          </button>
        </li>
      );
    });
  };

  return (
    <div className="flex flex-row justify-between items-center gap-4 w-full py-2">
      <div className="flex flex-row gap-x-4 items-center">
        <select
          id="itemsPerPage"
          value={itemsPerPage}
          onChange={(e) => onItemsPerPageChange(parseInt(e.target.value, 10))}
          className="relative flex items-right text-center justify-center text-xs font-medium border-gray-400 border-[1.5px] min-w-[2rem] px-1 py-1 rounded-md outline-none hover:bg-gray-500/5 focus:bg-purple-500/10 focus:ring-2 focus:ring-purple-500 dark:hover:bg-gray-400/5 transition text-purple-900"
        >
          <option value={25}>25</option>
          <option value={50}>50</option>
          <option value={100}>100</option>
          <option value={200}>200</option>
          <option value={500}>500</option>
          <option value={1000}>1000</option>
          <option value={0}>All</option>
        </select>
        <div className="flex items-center justify-center">
          <div className="border rounded-lg dark:border-gray-600">
            <ol className="flex items-center text-xs text-gray-700 divide-x rtl:divide-x-reverse divide-gray-300 dark:text-gray-400 dark:divide-gray-600 space-x-1 p-[1px]">
              <li>
                <button
                  type="button"
                  onClick={() => onPageChange(currentPage - 1)}
                  className={`relative flex items-center justify-center font-medium min-w-[2rem] px-1 py-1 rounded-md outline-none bg-white hover:bg-gray-500/5 focus:bg-purple-500/10 dark:hover:bg-gray-400/5 transition text-purple-900 ${
                    currentPage === 1 ? "cursor-not-allowed opacity-50" : ""
                  }`}
                  aria-label="Previous"
                  rel="prev"
                  disabled={currentPage === 1}
                >
                  <svg
                    className="w-5 h-5 rtl:scale-x-[-1]"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      fillRule="evenodd"
                      d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
                      clipRule="evenodd"
                    ></path>
                  </svg>
                </button>
              </li>
              {renderPageNumbers()}
              <li>
                <button
                  type="button"
                  onClick={() => onPageChange(currentPage + 1)}
                  className={`relative flex items-center justify-center font-medium min-w-[2rem] px-1 mx-1 py-1 rounded-md outline-none bg-white hover:bg-gray-500/5 focus:bg-purple-500/10 focus:ring-2 focus:ring-purple-500 dark:hover:bg-gray-400/5 transition text-purple-900 ${
                    currentPage === totalPages
                      ? "cursor-not-allowed opacity-50"
                      : ""
                  }`}
                  aria-label="Next"
                  rel="next"
                  disabled={currentPage === totalPages}
                >
                  <svg
                    className="w-5 h-5 rtl:scale-x-[-1]"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      fillRule="evenodd"
                      d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                      clipRule="evenodd"
                    ></path>
                  </svg>
                </button>
              </li>
            </ol>
          </div>
        </div>
      </div>
      <div className="font-semibold text-xs italic">
        Page {currentPage} of {totalPages} ({total_entries} entries)
      </div>
    </div>
  );
};

export default Pagination;
