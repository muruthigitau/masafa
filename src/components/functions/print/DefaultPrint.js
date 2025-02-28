import { toTitleCase } from "@/utils/textConvert";
import React, { useEffect, useState } from "react";

const CONTENT_PADDING = 10;
const PAGE_HEIGHT = 297;
const PAGE_WIDTH = 210;
const CONTENT_HEIGHT_RATIO = 0.9;
const PAGE_HEIGHT_PX = PAGE_HEIGHT * 3.77953;
const PAGE_WIDTH_PX = PAGE_WIDTH * 3.77953;
const CONTENT_HEIGHT_PX = PAGE_HEIGHT_PX * CONTENT_HEIGHT_RATIO;

const DefaultPrint = React.forwardRef(({ data, title, load }, ref) => {
  const [pages, setPages] = useState([]);
  const [currentDateTime, setCurrentDateTime] = useState("");
  const [isLandscape, setIsLandscape] = useState(false);

  useEffect(() => {
    const now = new Date();
    const options = {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    };
    setCurrentDateTime(now.toLocaleDateString("en-US", options));

    const calculatePages = () => {
      const filteredData = data
        ? Object.entries(data).filter(
            ([key]) =>
              key !== "id" && key !== "modified_at" && key !== "created_at"
          )
        : [];

      const contentContainer = document.createElement("div");
      contentContainer.style.width = `${PAGE_WIDTH_PX}px`;
      contentContainer.style.position = "absolute";
      contentContainer.style.top = "0";
      contentContainer.style.left = "0";
      contentContainer.style.visibility = "hidden";
      document.body.appendChild(contentContainer);

      const pagesArr = [];
      let currentPageContent = [];
      let currentHeight = 0;

      let nonArrayItems = []; // Array to track non-array items

      filteredData.forEach(([key, value], idx) => {
        if (Array.isArray(value)) {
          const isLandscapeMode = value.length > 3;
          if (isLandscapeMode & !isLandscape) {
            setIsLandscape(isLandscapeMode);
          }
        } else {
          nonArrayItems.push({ key, value });
        }
      });

      const nonArrayItemsPerPage = isLandscape ? 4 : 2;
      const nonArrayItemsCount = nonArrayItems.length;
      for (let i = 0; i < nonArrayItemsCount; i += nonArrayItemsPerPage) {
        const itemsToProcess = nonArrayItems.slice(i, i + nonArrayItemsPerPage);

        const contentHtml = `
          <div class="grid grid-cols-${nonArrayItemsPerPage} gap-x-4 text-xs text-darkblack-900">
           ${itemsToProcess
             .map(
               (item) => `
              <div class="flex flex-row justify-between w-full rounded px-1 py-1 my-1">
                <div class="flex-none w-full px-1">
                  <div>
                    <p class="mb-0 font-sans text-xs font-medium leading-normal">
                      ${toTitleCase(item.key)}
                    </p>
                    <h5 class="mb-0 font-bold">${item.value}</h5>
                  </div>
                </div>
              </div>
            `
             )
             .join("")}
          </div>
          `;

        const contentDiv = document.createElement("div");
        contentDiv.style.marginBottom = "20px";
        contentDiv.innerHTML = contentHtml;

        contentContainer.appendChild(contentDiv);
        currentHeight = contentContainer.scrollHeight;

        if (currentHeight > CONTENT_HEIGHT_PX - 2 * CONTENT_PADDING) {
          pagesArr.push(currentPageContent);
          currentPageContent = [contentDiv.innerHTML];
          contentContainer.innerHTML = "";
          contentContainer.appendChild(contentDiv);
          currentHeight = contentContainer.scrollHeight;
        } else {
          currentPageContent.push(contentDiv.innerHTML);
        }
      }

      // Process array items
      filteredData.forEach(([key, value], idx) => {
        if (Array.isArray(value)) {
          const arrayFields = Object.keys(value[0] || {}).filter(
            (field) => field !== "modified_at" && field !== "created_at"
          );
          const columnCount = arrayFields.length * 2 + 3;
          const gridTemplateColumns = `repeat(${columnCount}, 1fr)`;

          const tableHeader = `
          <div class="text-left pt-4 font-semibold">${toTitleCase(key)}</div>
            <table class="min-w-full mt-2 rounded-t-sm text-xs overflow-hidden">
            <thead>
              <tr
              class="bg-gray-100 border-b-[1px] border-gray-300 justify-center"
              style="display: grid; grid-template-columns: ${gridTemplateColumns};" 
              >
                <th class="py-2 px-1 text-center font-bold col-span-1">No.</th>
                ${arrayFields
                  .map(
                    (field) =>
                      `<th class="py-2 px-1 text-center font-bold col-span-2 break-words">${toTitleCase(
                        field
                      )}</th>`
                  )
                  .join("")}
              </tr>
            </thead>
            <tbody>
        `;
          const tableFooter = `</tbody></table>`;

          currentPageContent.push(tableHeader);

          value.forEach((item, index) => {
            const rowClasses = index % 2 === 0 ? "bg-gray-50" : "bg-white";
            const contentHtml = `
              <div class="${rowClasses} justify-center border-b border-gray-100 text-[12px]"
                 style="display: grid; grid-template-columns: ${gridTemplateColumns};">
                <div class="py-2 px-1 text-center text-darkblack-900 font-medium border-r border-gray-100">
                  ${index + 1}
                </div>
                ${arrayFields
                  .map(
                    (field) =>
                      `<div class="py-2 px-1 text-left text-darkblack-800 border-l border-gray-100 col-span-2 break-words">${
                        item[field] || ""
                      }</div>`
                  )
                  .join("")}
              </div>
            `;

            const contentDiv = document.createElement("div");
            contentDiv.style.marginBottom = "20px";
            contentDiv.innerHTML = contentHtml;

            contentContainer.appendChild(contentDiv);
            currentHeight = contentContainer.scrollHeight;

            if (currentHeight > CONTENT_HEIGHT_PX - 2 * CONTENT_PADDING) {
              currentPageContent.push(tableFooter);
              pagesArr.push(currentPageContent);
              currentPageContent = [tableHeader, contentDiv.innerHTML];
              contentContainer.innerHTML = "";
              contentContainer.appendChild(contentDiv);
              currentHeight = contentContainer.scrollHeight;
            } else {
              currentPageContent.push(contentDiv.innerHTML);
            }
          });

          currentPageContent.push(tableFooter);
        }
      });

      if (currentPageContent.length > 0) {
        pagesArr.push(currentPageContent);
      }

      document.body.removeChild(contentContainer);
      setPages(pagesArr);
    };

    calculatePages();
  }, [load, data]);

  const pageWidth = isLandscape ? PAGE_HEIGHT : PAGE_WIDTH;
  const pageHeight = isLandscape ? PAGE_WIDTH : PAGE_HEIGHT;

  return (
    <div ref={ref} style={{ width: `${pageWidth}mm`, margin: "0 auto" }}>
      {data &&
        pages?.map((pageData, pageIndex) => (
          <div
            key={pageIndex}
            className="relative bg-white text-black print:w-[210mm] print:h-[297mm] print:overflow-hidden"
            style={{
              width: `${pageWidth}mm`,
              height: `${pageHeight}mm`,
              margin: "0 auto",
              pageBreakAfter: pageIndex < pages.length - 1 ? "always" : "auto",
              display: "flex",
              flexDirection: "column",
            }}
          >
            {/* Header Section */}
            <div className="flex flex-col items-center justify-center py-4 border-b border-gray-300">
              <h1 className="text-xl font-bold">Masafa Logistics</h1>
              <p className="text-xs">
                Your Trusted Partner in Logistics Solutions
              </p>
            </div>

            {/* Content Section */}
            <div
              className="flex-1 flex flex-col mx-8 my-4 items-center justify-start"
              style={{
                paddingTop: CONTENT_PADDING,
                paddingBottom: CONTENT_PADDING,
                overflow: "hidden",
              }}
            >
              <div className="flex flex-wrap gap-x-2 items-center justify-center">
                {pageIndex === 0 && title && (
                  <h2 className="text-xl font-bold text-center mb-2">
                    {title}
                  </h2>
                )}
                {pageIndex === 0 && data?.id && (
                  <h2 className="text-xl font-semibold text-center mb-2">
                    {data.id}
                  </h2>
                )}
              </div>
              <div className="w-full">
                {pageData?.map((contentHtml, index) => (
                  <div
                    key={index}
                    dangerouslySetInnerHTML={{ __html: contentHtml }}
                  />
                ))}
              </div>
            </div>

            {/* Footer Section */}
            <p className="text-xs pb-1 text-center">Page {pageIndex + 1}</p>
            <div className="flex flex-col text-black items-center justify-center py-2 border-t border-gray-300">
              <p className="text-xs">Generated on: {currentDateTime}</p>
              <p className="text-xs pb-2">
                Blue Sky Filling Station, Ngara park Road, Nairobi Telephone:
                +254711595716
              </p>
            </div>
          </div>
        ))}
    </div>
  );
});

export default DefaultPrint;
