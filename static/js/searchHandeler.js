document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("search-form");
    const input = document.getElementById("myInput");
    const dropdown = document.getElementById("searchDropdown");
  
    function renderResults(results) {
      dropdown.innerHTML = ""; // Clear previous results
  
      if (results.length === 0) {
        dropdown.style.display = "block";
        dropdown.innerHTML = '<li class="dropdown-item text-muted">No results found.</li>';
        return;
      }
  
      results.forEach(item => {
        const li = document.createElement("li");
        li.className = "dropdown-item p-2";
  
        li.innerHTML = `
        <a class="text-decoration-none text-black" href="/productview/${item.id}"
          <div class="product-item d-flex align-items-center">
            <div class="product-image" style="flex-shrink: 0; width: 100px; height: 100px; overflow: hidden;">
              <img src="${item.image}" alt="${item.title}" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <div class="product-info ms-3">
              <h5 class="product-name mb-2 text-wrap">${item.title}</h5>
              <p class="product-price mb-0">₹${item.discounted_price}
                <small style="text-decoration:line-through; color:gray;">₹${item.price}</small>
              </p>
            </div>
          </div>
        `;
        dropdown.appendChild(li);
      });
  
      dropdown.style.display = "block"; // Show dropdown
    }
  
    function performSearch(query) {
      if (!query) {
        dropdown.style.display = "none";
        dropdown.innerHTML = "";
        return;
      }
  
      fetch(`/search/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => renderResults(data.results))
        .catch(err => {
          console.error("Search error:", err);
          dropdown.innerHTML = '<li class="dropdown-item text-danger">Error occurred.</li>';
          dropdown.style.display = "block";
        });
    }
  
    // Live search
    input.addEventListener("input", () => {
      performSearch(input.value.trim());
    });
  
    // Handle submit
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      performSearch(input.value.trim());
    });
  
    // Optional: Hide dropdown when clicking outside
    document.addEventListener("click", function (e) {
      if (!form.contains(e.target)) {
        dropdown.style.display = "none";
      }
    });
  });