import { Html, Head, Main, NextScript } from "next/document";

export default function Document() {
  return (
    <Html lang="en">
      <Head>
        <title>
          Masafa Logistics - Streamlined and Reliable Logistics Solutions
        </title>

        {/* SEO Meta Tags */}
        <meta
          name="description"
          content="Masafa Logistics - Providing efficient and scalable logistics solutions for businesses worldwide."
        />
        <meta
          name="keywords"
          content="Masafa Logistics, logistics solutions, supply chain management, shipping, freight forwarding, transportation, warehouse management, logistics software"
        />
        <meta name="author" content="Masafa Logistics" />

        {/* Open Graph Meta Tags for SMO */}
        <meta
          property="og:title"
          content="Masafa Logistics - Streamlined and Reliable Logistics Solutions"
        />
        <meta
          property="og:description"
          content="Optimize your logistics and supply chain operations with Masafa Logistics, a comprehensive solution for businesses in need of reliable, cost-effective transport and logistics services."
        />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="https://www.masafalogistics.com" />
        <meta
          property="og:image"
          content="https://masafalogistics.com/masafa-logo.png"
        />
        <meta property="og:site_name" content="Masafa Logistics" />

        {/* Twitter Card Meta Tags */}
        <meta name="twitter:card" content="summary_large_image" />
        <meta
          name="twitter:title"
          content="Masafa Logistics - Streamlined and Reliable Logistics Solutions"
        />
        <meta
          name="twitter:description"
          content="Masafa Logistics offers scalable logistics solutions designed to optimize shipping, supply chain management, and more for businesses globally."
        />
        <meta
          name="twitter:image"
          content="https://masafalogistics.com/masafa-logo.png"
        />
        <meta name="twitter:site" content="@MasafaLogistics" />

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
