document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/currency-table')
        .then(response => response.json())
        .then(data => {
            let main_page_currency_table = data["main_page_currency_table"];
            const container = document.getElementById('table-container');
            const table = document.createElement('table');
            
            // Create headers
            const headers = Object.keys(main_page_currency_table[0]);
            const headerRow = document.createElement('tr');
            headers.forEach(header => {
                const th = document.createElement('th');
                th.textContent = header;
                headerRow.appendChild(th);
            });
            table.appendChild(headerRow);

            // Create rows with click handlers
            main_page_currency_table.forEach(item => {
                const tr = document.createElement('tr');
                tr.style.cursor = 'pointer';  // Show pointer cursor
                
                // Add data attribute for currency identifier (e.g., "USD")
                tr.setAttribute('data-currency', item.Currency);  // Replace "Currency" with your actual column name
                
                headers.forEach(header => {
                    const td = document.createElement('td');
                    td.textContent = item[header];
                    tr.appendChild(td);
                });

                // Add click handler
                tr.addEventListener('click', () => {
                    const currency = tr.getAttribute('data-currency');
                    window.location.href = `/${currency}`;  // Navigate to Flask route
                });

                table.appendChild(tr);
            });

            container.appendChild(table);
        })
        .catch(error => console.error('Error:', error));
});