import path from "path";
import fs from "fs";

// Define the root path for apps
const basePath = path.join(process.cwd());

// Load the site configuration
const siteConfigPath = path.join(process.cwd(), "sites", "sites.json");
const siteConfig = JSON.parse(fs.readFileSync(siteConfigPath, "utf8"));

// Load the doctypes data
const doctypeConfigPath = path.join(basePath, "sites", "doctypes.json");
const doctypesData = JSON.parse(fs.readFileSync(doctypeConfigPath, "utf8"));

// Helper function to normalize and clean the search keyword
const cleanKeyword = (keyword) => {
  let cleanedKeyword = keyword.trim().toLowerCase();

  // Remove "New" at the beginning or "List" at the end if present
  if (cleanedKeyword.startsWith("new ")) {
    cleanedKeyword = cleanedKeyword.slice(4).trim(); // Remove 'new'
  }
  if (cleanedKeyword.endsWith(" list")) {
    cleanedKeyword = cleanedKeyword.slice(0, -5).trim(); // Remove 'list'
  }

  return cleanedKeyword;
};

// Helper function to perform advanced fuzzy matching
const isFuzzyMatch = (str, keyword) => {
  return str.toLowerCase().includes(keyword);
};

export default async function handler(req, res) {
  const { keyword } = req.query;

  if (!keyword) {
    return res.status(400).json({ message: "Keyword is required" });
  }

  // Clean and prepare the search keyword for matching
  const cleanedKeyword = cleanKeyword(keyword);

  // Array to hold the matched documents
  let matchedDocs = [];

  // Iterate through the installed apps to find matching doctypes
  for (const appData of doctypesData) {
    // Find the app in the doctypes data
    // const appData = doctypesData.find((appEntry) => appEntry.id === app.id);

    if (appData) {
      // Iterate through the modules and their docs
      for (const module of appData.modules) {
        for (const doc of module.docs) {
          // Check for partial matches for both doc id and doc name
          const matchId = isFuzzyMatch(doc.id, cleanedKeyword);
          const matchName = isFuzzyMatch(doc.name, cleanedKeyword);

          if (matchId || matchName) {
            // Add the matched document to the results
            matchedDocs.push({
              app: appData.name,
              app_id: appData.id,
              module_id: module.id,
              module: module.name,
              id: doc.id,
              name: doc.name,
            });
          }
        }
      }
    }
  }

  // Check if any matches were found
  if (matchedDocs.length > 0) {
    return res.status(200).json(matchedDocs);
  } else {
    return res.status(200).json([]); // Return an empty array if no matches
  }
}
