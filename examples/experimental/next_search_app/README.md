# Parcl Labs Next.js App

## Overview

This is a [Next.js](https://nextjs.org/) project that utilizes the Parcl Labs Price Feed (PLPF) Search API to provide real-time residential real estate price tracking. The application allows users to perform searches and view results in an interactive table. Data can also be exported to CSV for further analysis.

## Features

- Real-time real estate price tracking using the Parcl Labs Search API
- Interactive table to display search results
- CSV export functionality

## Getting Started

To set up the project locally:

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd <repo-folder>

2. **Generate an API Key:**
- Sign up at Parcl Labs Dashboard to obtain your API key.

3. **Create a .env.local file:**

- Copy the contents of .env.example to a new file named .env.local.

4. Add your API key to .env.local:
   ```bash
   NEXT_PUBLIC_PARCLLABS_API_KEY=your_api_key_here


5. Install dependencies:
   ```bash
   npm install

6. Run the development server:
   ```bash
   npm run dev

7. Access the application:
- Open http://localhost:3000 in your browser to use the app.

## Usage

1. Enter search queries into the provided form.
2. Fetch real estate data and view results in the interactive table.
3. Export the data to a CSV file for further analysis.

## Demo

🔗 [Link to Demo](https://parcllabs-next.vercel.app/)

This application is deployed to Vercel for easy access and demonstration.


## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Author

Created by Tina Park. Check out my portfolio at [tinapark.dev](https://tinapark.dev).
