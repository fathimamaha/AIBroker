'use strict';
const express = require('express');
const path = require('path');
const app = express();
const port = 3000;

// Configuration for the Python backend
const PYTHON_BACKEND_URL = 'http://localhost:12345';

// Configuration for polling
const POLLING_INTERVAL_MS = 15000; // 2 seconds
const POLLING_TIMEOUT_MS = 120000; // 2 minutes

app.use(express.static('public'));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/query.html', async (req, res) => {

  const searchQuery = req.query.q;

  if (!searchQuery) {
    return res.status(400).send('<h1>Error: No search query provided.</h1>');
  }
  try {
    // --- Step 1: Submit the query and get a query ID ---
    console.log(`Submitting query to backend: "${searchQuery}"`);
    const submitResponse = await fetch(`${PYTHON_BACKEND_URL}/submit_query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: searchQuery }),
    });

    if (!submitResponse.ok) {
      throw new Error(`Backend submission failed with status: ${submitResponse.status}`);
    }

    const { query_id } = await submitResponse.json();
    console.log(`Received query_id: ${query_id}`);

    // --- Step 2: Poll for the result ---
    let finalResult = null;
    const startTime = Date.now();

    while (Date.now() - startTime < POLLING_TIMEOUT_MS) {
      console.log(`Polling for result for query_id: ${query_id}`);
      const getResultResponse = await fetch(`${PYTHON_BACKEND_URL}/get_query_response/${query_id}`);

      if (getResultResponse.status === 200) {
        // Found the result, break the loop
        finalResult = await getResultResponse.json();
        console.log('Result found:', finalResult);
        break;
      } else if (getResultResponse.status === 202) {
        // 202 Accepted means the job is still processing, wait and continue
        console.log('Result not ready yet (202). Waiting...');
        await new Promise(resolve => setTimeout(resolve, POLLING_INTERVAL_MS));
      } else {
        // Handle other unexpected statuses
        throw new Error(`Backend polling failed with status: ${getResultResponse.status}`);
      }
    }

    // --- Step 3: Render the final HTML ---
    if (finalResult) {
      const resultsHtml = generateResultsHtml(finalResult, searchQuery);
      res.send(resultsHtml);
    } else {
      // If the loop finishes without a result, it timed out
      console.error('Polling timed out.');
      res.status(408).send('<h1>Request timed out. The server is taking too long to respond.</h1>');
    }

  } catch (error) {
    console.error('An error occurred:', error);
    res.status(500).send(`<h1>An error occurred while contacting the backend: ${error.message}</h1>`);
  }
});

/**
 * Generates the final HTML to be displayed in the iframe.
 * @param {object} data - The data object from the backend ({ content, image, url }).
 * @param {string} query - The original search query.
 * @returns {string} - The complete HTML string.
 */
function generateResultsHtml(data, query) {
  const { content, image, url } = data;
  return `
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Query Results</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Poppins', sans-serif; background-color: #f8fafc; color: #1e293b; margin: 0; }
        </style>
    </head>
    <body>
        <div class="flex flex-col lg:flex-row gap-6 p-4">
            <!-- Left Panel: Text Response -->
            <div class="lg:w-2/3 flex flex-col bg-white rounded-2xl shadow-md border border-slate-200 overflow-hidden">
                <div class="p-5 flex-grow"><p class="text-slate-600 leading-relaxed">${content || 'No content provided.'}</p></div>
            </div>

            <!-- Right Panel: Images -->
            <div class="lg:w-1/3 flex flex-col bg-white rounded-2xl shadow-md border border-slate-200 overflow-hidden">
                <div class="p-5 flex-grow">
                    <div class="grid">
                        <img src="${image}" alt="Image for ${query}" class="w-full h-auto object-cover rounded-lg" onerror="this.style.display='none'">
                    </div>
                </div>
            </div>
        </div>

        <!-- Footer Section: URLs -->
        <footer class="w-full max-w-7xl mx-auto mt-0 lg:mt-6 p-4">
          <div class="bg-white rounded-2xl shadow-md border border-slate-200 overflow-hidden">
              <div class="p-5 border-b border-slate-200"><h3 class="text-xl font-semibold text-slate-700">More Details</h3></div>
              <div class="p-5">
                  <ul class="list-disc list-inside space-y-2">
                      <li class="text-slate-600"><a href="${url}" target="_blank" class="text-blue-500 hover:underline">${url}</a></li>
                  </ul>
              </div>
          </div>
        </footer>
    </body>
    </html>
  `;
}


app.listen(port, () => {
  console.log(`AIBroker app listening at http://localhost:${port}`);
});