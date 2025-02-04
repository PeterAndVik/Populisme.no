document.addEventListener("DOMContentLoaded", function () {
    // ✅ Fetch the list of graph files
    fetch("graphs/")
        .then(response => response.text())
        .then(html => {
            // ✅ Extract filenames from the directory listing
            let parser = new DOMParser();
            let doc = parser.parseFromString(html, "text/html");
            let links = doc.querySelectorAll("a");

            let graphContainer = document.getElementById("graphs-container");

            links.forEach(link => {
                let filename = link.getAttribute("href");

                if (filename.endsWith(".html")) { // ✅ Only add .html files
                    let graphCard = document.createElement("div");
                    graphCard.className = "graph-card";

                    let graphTitle = document.createElement("h2");
                    graphTitle.textContent = filename.replace(".html", ""); // Remove .html from title

                    let iframe = document.createElement("iframe");
                    iframe.src = "graphs/" + filename;
                    iframe.width = "800";
                    iframe.height = "600";

                    graphCard.appendChild(graphTitle);
                    graphCard.appendChild(iframe);
                    graphContainer.appendChild(graphCard);
                }
            });
        })
        .catch(error => console.error("Error loading graphs:", error));
});
