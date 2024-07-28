// pages/api/proxy.ts

import type { NextApiRequest, NextApiResponse } from "next";

const handler = async (req: NextApiRequest, res: NextApiResponse) => {
  // Define the API endpoint to forward the request to
  const apiUrl = "https://api.parcllabs.com/v1/search/markets";

  // Extract query parameters from the request
  const { query } = req;

  // Construct the URL for the API request
  const url = new URL(apiUrl);
  url.search = new URLSearchParams(query as Record<string, string>).toString();

  try {
    // Fetch data from the external API
    const response = await fetch(url.toString(), {
      method: req.method,
      headers: {
        Authorization: `${process.env.NEXT_PUBLIC_PARCLLABS_API_KEY}`,
        Accept: "application/json",
      },
    });

    // Check for successful response
    if (!response.ok) {
      throw new Error(`Error fetching data: ${response.statusText}`);
    }

    // Return the response data
    const data = await response.json();
    console.log("Data:", data); // Debug: log the data received
    console.log("URL:", url.toString()); // Debug: log the URL used
    res.status(200).json(data);
  } catch (error) {
    if (error instanceof Error) {
      res.status(500).json({ error: error.message });
    } else {
      // Handle unexpected error types
      res.status(500).json({ error: "An unknown error occurred" });
    }
  }
};

export default handler;
