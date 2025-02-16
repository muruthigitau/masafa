import { Html, Head, Main, NextScript } from "next/document";

export default function Document() {
  return (
    <Html lang="en">
      <Head>
        <title>Blox ERP - Comprehensive and Adaptable ERP Solution</title>

        {/* SEO Meta Tags */}
        <meta
          name="description"
          content="Blox ERP - A scalable and customizable enterprise resource planning solution designed for diverse industries."
        />
        <meta
          name="keywords"
          content="Blox ERP, enterprise resource planning, ERP software, business management, CRM, HR, inventory management, supply chain, manufacturing, financial management"
        />
        <meta name="author" content="Blox ERP" />

        {/* Open Graph Meta Tags for SMO */}
        <meta
          property="og:title"
          content="Blox ERP - Comprehensive and Adaptable ERP Solution"
        />
        <meta
          property="og:description"
          content="Streamline your business operations with Blox ERP, the flexible and scalable ERP solution tailored for all industries."
        />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="https://www.bloxerp.com" />
        <meta
          property="og:image"
          content="https://test.bloxerp.com/blox-logo.png"
        />
        <meta property="og:site_name" content="Blox ERP" />

        {/* Twitter Card Meta Tags */}
        <meta name="twitter:card" content="summary_large_image" />
        <meta
          name="twitter:title"
          content="Blox ERP - Comprehensive and Adaptable ERP Solution"
        />
        <meta
          name="twitter:description"
          content="Blox ERP offers a modular, scalable ERP solution designed to manage business operations across various industries."
        />
        <meta
          name="twitter:image"
          content="https://test.bloxerp.com/blox-logo.png"
        />
        <meta name="twitter:site" content="@BloxERP" />

        {/* Existing links and scripts */}
        <link
          href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,600,700"
          rel="stylesheet"
        />
        <script
          async
          src="https://kit.fontawesome.com/42d5adcbca.js"
          crossOrigin="anonymous"
        ></script>
        <link href="/css/nucleo-icons.css" rel="stylesheet" />
        <link href="/css/nucleo-svg.css" rel="stylesheet" />
        <link
          href="/css/soft-ui-dashboard-tailwind.css?v=1.0.5"
          rel="stylesheet"
        />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
