export function getTenant() {
  return "masafa"
  // if (typeof window !== "undefined") {
  //   // Client-side: Get tenant from subdomain
  //   const host = window.location.hostname;
  //   const subdomain = host.split(".")[0]; // e.g., "ten1.localhost" → "ten1"
  //   return subdomain !== "localhost" ? subdomain : "default";
  // }
  // return "default"; // Default tenant if running in a non-browser environment
}
