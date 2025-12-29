async function uploadFile(file, sessionName) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('session_name', sessionName);
    
    // UI Updates
    document.getElementById('loader').style.display = 'block';
    document.getElementById('error-message').style.display = 'none';

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            window.location.href = `/results?session_id=${data.session_id}`;
        } else {
            throw new Error(data.detail || 'Upload failed');
        }
    } catch (error) {
        document.getElementById('error-message').innerText = error.message;
        document.getElementById('error-message').style.display = 'block';
    } finally {
        document.getElementById('loader').style.display = 'none';
    }
}

// NOTE: I wrote 'async def' above by Python habit, JS is 'async function'
// Correcting logic in valid JS syntax below for the file write.

const API_BASE = '/api/analysis';

async function loadDashboard(sessionId) {
    // Load independent sections in parallel without blocking each other
    // We don't await them here so they render as soon as they are ready
    loadOverview(sessionId).catch(e => console.error("Overview error:", e));
    loadStats(sessionId).catch(e => console.error("Stats error:", e));
    loadVisualizations(sessionId).catch(e => console.error("Viz error:", e));
    
    // Save id
    window.currentSessionId = sessionId;
}

async function loadOverview(sessionId) {
    try {
        console.log("Fetching overview for " + sessionId);
        const res = await fetch(`${API_BASE}/${sessionId}/overview`);
        console.log("Overview response status:", res.status);
        if (!res.ok) {
            let errorMsg = res.statusText;
            try {
                const errorData = await res.json();
                if (errorData.detail) errorMsg = errorData.detail;
            } catch(e) {} // Ignore json parse error if body is empty
            
            if (res.status === 404) {
                 alert("Session expired. Please upload again.");
                 window.location.href = '/upload';
                 return;
            }
            throw new Error(`Failed to load overview: ${errorMsg}`);
        }
        const data = await res.json();
        console.log("Overview data received");
        
        // Info Container
        const infoHtml = `
            <p><strong>Rows:</strong> ${data.shape[0]}</p>
            <p><strong>Columns:</strong> ${data.shape[1]}</p>
            <p><strong>Memory Usage:</strong> ${(data.info.memory_usage / 1024).toFixed(2)} KB</p>
        `;
        document.getElementById('info-container').innerHTML = infoHtml;
        
        // Head Table
        renderTable(data.head, 'head-container');
    } catch (e) {
        document.getElementById('info-container').innerHTML = `<p style="color:red">Error: ${e.message}</p>`;
        document.getElementById('head-container').innerHTML = `<p style="color:red">Error loading data sample.</p>`;
    }
}


async function loadStats(sessionId) {
    try {
        console.log("Fetching stats for " + sessionId);
        const res = await fetch(`${API_BASE}/${sessionId}/stats`);
        console.log("Stats response status:", res.status);
        if (!res.ok) {
            let errorMsg = res.statusText;
            try {
                const errorData = await res.json();
                if (errorData.detail) errorMsg = errorData.detail;
            } catch(e) {}

            throw new Error(`Failed to load statistics: ${errorMsg}`);
        }
        
        const data = await res.json();
        console.log("Stats data received");
        window.statsData = data; 

        // Missing Values
        const missing = data.missing_values.count;
        let missingHtml = '<ul>';
        let hasMissing = false;
        for (const [col, count] of Object.entries(missing)) {
            if (count > 0) {
                missingHtml += `<li><strong>${col}:</strong> ${count}</li>`;
                hasMissing = true;
            }
        }
        missingHtml += '</ul>';
        document.getElementById('missing-container').innerHTML = hasMissing ? missingHtml : '<p>No missing values found!</p>';
        
        // Description Table
        renderDescribeTable(data.description, 'stats-container');
    } catch (e) {
         document.getElementById('stats-container').innerHTML = `<p style="color:red">Error: ${e.message}</p>`;
         document.getElementById('missing-container').innerHTML = `<p style="color:red">Error loading missing info.</p>`;
    }
}


async function loadVisualizations(sessionId) {
    const res = await fetch(`${API_BASE}/${sessionId}/visualizations`);
    if (!res.ok) {
        // Visualizations might fail if data is weird, still want to show other parts
        console.error("Viz load failed");
        document.getElementById('viz-container').innerHTML = '<p>Could not generate visualizations.</p>';
        return; 
    }
    const data = await res.json();
    
    // Viz data is name -> base64 string
    // We want to link this back to column stats for AI.
    // We assume the key "hist_ColumnName" or "bar_ColumnName" pattern
    
    const container = document.getElementById('viz-container');
    container.innerHTML = '';
    
    for (const [name, src] of Object.entries(data)) {
        const div = document.createElement('div');
        div.className = 'card';
        // Parse column name from key (e.g., hist_Age -> Age)
        let cleanName = name;
        let chartType = 'Chart';
        let colName = '';

        if(name.startsWith('hist_')) {
            colName = name.replace('hist_', '');
            cleanName = `Distribution of ${colName}`;
            chartType = 'Histogram';
        } else if (name.startsWith('bar_')) {
            colName = name.replace('bar_', '');
            cleanName = `Categories in ${colName}`;
            chartType = 'Bar Chart';
        } else if (name === 'correlation_heatmap') {
            cleanName = 'Correlation Heatmap';
            chartType = 'Heatmap';
        }

        const aiId = `ai-viz-${name}`;

        div.innerHTML = `
            <div class="card-title" style="font-size: 1rem; border: none; margin-bottom: 0.5rem; display:flex; justify-content:space-between;">
                ${cleanName}
                <button class="ai-btn" onclick="analyzeViz('${colName}', '${chartType}', '${aiId}')">✨</button>
            </div>
            <img src="${src}" class="viz-img" alt="${name}">
            <div id="${aiId}" class="ai-summary-box"></div>
        `;
        container.appendChild(div);
    }
}

async function analyzeSection(type, containerId) {
    const container = document.getElementById(containerId);
    
    // Toggle if already visible
    if(container.style.display === 'block' && container.classList.contains('active')) {
        container.style.display = 'none';
        container.classList.remove('active');
        return;
    }
    
    const apiKey = document.getElementById('api-key').value;
    // IF apiKey is empty, we send empty string, backend will try to use stored key.
    
    container.style.display = 'block';
    container.classList.add('active');
    container.innerHTML = 'Thinking... (AI is analyzing data)';
    
    let context = {};
    if (type === 'missing') {
        context = window.statsData.missing_values;
    } else if (type === 'stats') {
        context = window.statsData.description;
    }
    
    try {
        const payload = {
            api_key: apiKey,
            provider: 'gemini',
            prompt_type: type,
            context_data: context
        };
        
        await callAI(payload, container);
    } catch (e) {
        container.innerHTML = "Error: " + e.message;
    }
}

async function analyzeViz(colName, chartType, containerId) {
    const container = document.getElementById(containerId);
    if(container.style.display === 'block') {
        container.style.display = 'none';
        return;
    }
    
    const apiKey = document.getElementById('api-key').value;
    // IF apiKey is empty, we send empty string, backend will try to use stored key.

    container.style.display = 'block';
    container.classList.add('active');
    container.innerHTML = `Analyzing ${chartType}...`;
    
    // Prepare context: stats for this specific column if possible
    let stats = {};
    if (window.statsData && window.statsData.description && window.statsData.description[colName]) {
        stats = window.statsData.description[colName];
    }
    
    const payload = {
        api_key: apiKey,
        provider: 'gemini',
        prompt_type: 'visualization',
        context_data: {
            column: colName,
            type: chartType,
            stats: stats
        }
    };
    
    await callAI(payload, container);
}

async function callAI(payload, containerElement) {
    try {
        const res = await fetch('/api/ai/summarize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        if (!res.ok) throw new Error((await res.json()).detail);
        
        const data = await res.json();
        containerElement.innerHTML = marked.parse(data.summary);
        
    } catch (e) {
        containerElement.innerHTML = `<span style="color:red">Error: ${e.message}</span>`;
    }
}


// Helpers
function renderTable(dataArray, containerId) {
    if (!dataArray || dataArray.length === 0) {
        document.getElementById(containerId).innerHTML = '<p>No data available.</p>';
        return;
    }
    
    const headers = Object.keys(dataArray[0]);
    let html = '<table><thead><tr>';
    headers.forEach(h => html += `<th>${h}</th>`);
    html += '</tr></thead><tbody>';
    
    dataArray.forEach(row => {
        html += '<tr>';
        headers.forEach(h => {
             // Handle nulls
             const val = row[h] === null ? '<span style="color:#ccc">NaN</span>' : row[h];
             html += `<td>${val}</td>`;
        });
        html += '</tr>';
    });
    
    html += '</tbody></table>';
    document.getElementById(containerId).innerHTML = html;
}

function renderDescribeTable(descObj, containerId) {
    // descObj = { col1: {count: 10, mean: 5...}, ... }
    const columns = Object.keys(descObj);
    if (columns.length === 0) return;
    
    const statsNames = Object.keys(descObj[columns[0]]); // [count, mean, std...]
    
    let html = '<table><thead><tr><th>Stat</th>';
    columns.forEach(c => html += `<th>${c}</th>`);
    html += '</tr></thead><tbody>';
    
    statsNames.forEach(stat => {
        html += `<tr><td><strong>${stat}</strong></td>`;
        columns.forEach(col => {
            let val = descObj[col][stat];
            if (typeof val === 'number') val = val.toFixed(2);
            if (val === null || val === undefined) val = '-';
            html += `<td>${val}</td>`;
        });
        html += '</tr>';
    });
    html += '</tbody></table>';
    document.getElementById(containerId).innerHTML = html;
}

async function generateSummary() {
    const container = document.getElementById('ai-content');
    const loading = document.getElementById('ai-loading');
    const apiKey = document.getElementById('api-key').value;
    
    if (loading) loading.style.display = 'block';
    if (container) container.innerHTML = 'Thinking...';
    
    try {
        // Use stats data if available, otherwise simplified context
        let context = { note: "Please provide a general overview of the dataset." };
        if (window.statsData && window.statsData.description) {
            context = window.statsData.description;
        }
        
        const payload = {
            api_key: apiKey,
            provider: 'gemini',
            prompt_type: 'overview',
            context_data: context
        };
        
        await callAI(payload, container);
        
    } catch (e) {
        if (container) container.innerHTML = "Error: " + e.message;
    } finally {
        if (loading) loading.style.display = 'none';
    }
}

// Global scope expose
window.uploadFile = uploadFile;
window.loadDashboard = loadDashboard;
window.generateSummary = generateSummary;
window.analyzeSection = analyzeSection;
window.analyzeViz = analyzeViz;
