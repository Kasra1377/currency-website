// Get currency from URL path
const pathSegments = window.location.pathname.split('/');
const currency = pathSegments[pathSegments.length - 1];


document.addEventListener('DOMContentLoaded', () => {
    const apiUrl = `/api/currency/${currency}`;
    const container = document.getElementById('currency-indicator-table-container');

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            // Clear previous content
            container.innerHTML = '';

            // Create table element
            const table = document.createElement('table');
            table.style.borderCollapse = 'collapse';
            table.style.width = '100%';
            table.style.margin = '20px 0';

            // Create table rows
            for (const [key, valueObj] of Object.entries(data)) {
                const row = document.createElement('tr');
                
                // Create header cell
                const th = document.createElement('th');
                th.textContent = key;
                th.style.padding = '10px';
                th.style.border = '1px solid #ddd';
                th.style.textAlign = 'left';
                th.style.backgroundColor = '#f5f5f5';

                // Create data cell
                const td = document.createElement('td');
                td.textContent = valueObj["3"]; // Access the nested value
                td.style.padding = '10px';
                td.style.border = '1px solid #ddd';

                // Add cells to row
                row.appendChild(th);
                row.appendChild(td);
                
                // Add row to table
                table.appendChild(row);
            }

            // Add table to container
            container.appendChild(table);
        })
        .catch(error => {
            console.error('Error:', error);
            container.innerHTML = '<p>Error loading data</p>';
        });
})
