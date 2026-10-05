import { defineConfig } from "@canva/app-scripts";

export default defineConfig({
  config: (config, { mode }) => {
    // The development app reads the prepared textbook assets from this server.
    const origin = process.env.CANVA_APP_ORIGIN;
    if (
      mode === "development" &&
      origin &&
      /^https:\/\/app-[a-z0-9]+\.canva-apps\.com$/.test(origin)
    ) {
      config.server = {
        ...config.server,
        headers: { "Access-Control-Allow-Origin": origin },
      };
    }
    return config;
  },
});
