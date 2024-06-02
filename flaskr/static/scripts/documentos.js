buttons = document.getElementsByClassName("delete")

Array.from(buttons).forEach(button => {
    button.addEventListener('click', async () => {
        const url = '/api/document/' + button.name;
        fetch(url, {
            method: 'DELETE', // Specify DELETE method for removing data
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error deleting document: ${response.statusText}`);
                }
                window.location = window.location
            })
            .catch(error => console.error('Error:', error));
    })
});

link = document.getElementById("link")
selector = document.getElementById("designos")
selector2 = document.getElementById("documentos")

link.addEventListener('click', async () => {
    const selectedIndex = selector.selectedIndex;
    const selectedValue = selector.options[selectedIndex].value;

    const selectedIndex2 = selector2.selectedIndex;
    const selectedValue2 = selector2.options[selectedIndex2].value;
    const url = '/api/design_document';
    fetch(url, {
        method: 'POST', // Can be GET, POST, PUT, DELETE, etc.
        headers: {
          'Content-Type': 'application/json' // Specify JSON content type
        },
        body: JSON.stringify({ // Convert data to JSON string
          document_id: selectedValue2,
          design_id: selectedValue,
          name: "Связка" + selectedValue2 + "_" + selectedValue
        })
      })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error linking document: ${response.statusText}`);
            }
            window.location = window.location
        })
        .catch(error => console.error('Error:', error));
})