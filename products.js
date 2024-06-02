const api = "http://127.0.0.1:5000";

window.onload = () => {
    // BEGIN CODE HERE
    const searchButton = document.querySelector('button.btn-outline-primary');
    searchButton.addEventListener('click', searchButtonOnClick);

    const productForm = document.querySelector('form');
    productForm.addEventListener('submit', productFormOnSubmit);
    // END CODE HERE
}

searchButtonOnClick = () => {
    // BEGIN CODE HERE
    const nameInput = document.getElementById('searchName').value.trim();
    const tableBody = document.querySelector('tbody');
    fetch(`${api}/search?name=${nameInput}`)
        .then(response => {
            
            

            tableBody.innerHTML = ''; 
            return response.json();
        })
        .then(products => {
            products.forEach(product => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <th scope="row">${product.id}</th>
                    <td>${product.name}</td>
                    <td>${product.production_Year}</td>
                    <td>${product.price}</td>
                    <td>${product.color}</td>
                    <td>${product.size}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        
        .catch(error => {
            console.error('There was a problem with the search request:', error);
        });
    // END CODE HERE
}

productFormOnSubmit = (event) => {
    // BEGIN CODE HERE

    event.preventDefault(); 

    const nameInput = document.getElementById('name');
    const prYearInput = document.getElementById('prYear');
    const priceInput = document.getElementById('price');
    const colorInput = document.getElementById('color');
    const sizeInput = document.getElementById('size');

    const newProduct = {
        name: nameInput.value.trim(),
        production_Year: parseInt(prYearInput.value.trim(), 10),
        price: parseInt(priceInput.value.trim(), 10),
        color: parseInt(colorInput.value.trim(), 10),
        size: parseInt(sizeInput.value.trim(), 10)
        };
        fetch(`${api}/add-product`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newProduct),
        })
        .then(response => {
        
            return response.json();
        })
        .catch(error => {
            console.error('There was a problem with the product addition request:', error);
        });
    // END CODE HERE
}
