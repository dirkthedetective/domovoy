link = document.getElementById("link")
selector = document.getElementById("useros")
selector2 = document.getElementById("designos")

if (link) {
    link.addEventListener('click', async () => {
        const selectedIndex = selector.selectedIndex;
        const selectedValue = selector.options[selectedIndex].value;
    
        const selectedIndex2 = selector2.selectedIndex;
        const selectedValue2 = selector2.options[selectedIndex2].value;
        const url = '/api/order';
    
        fetch(url, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json' // Specify JSON content type
            },
            body: JSON.stringify({ // Convert data to JSON string
              client_id: selectedValue,
              design_id: selectedValue2,
            })
          })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error filing order: ${response.statusText}`);
                }
                window.location = window.location
            })
            .catch(error => console.error('Error:', error));
    })
}

radio = document.getElementsByClassName("status")

Array.from(radio).forEach(button => {
    button.addEventListener('click', () => {

        const selectedValue = button.value;
        const selectedValue2 = button.getAttribute("name");
        const url = '/api/status';

        fetch(url, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json' // Specify JSON content type
            },
            body: JSON.stringify({ // Convert data to JSON string
              order_status: selectedValue,
              id: selectedValue2,
            })
          })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error changing status: ${response.statusText}`);
                }
                window.location = window.location
            })
            .catch(error => console.error('Error:', error));
    })
});
