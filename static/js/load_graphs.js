document.addEventListener("DOMContentLoaded", function () {
    fetch("graphs/graphs.json")  // ✅ Fetch the list of graphs from the JSON file
        .then(response => response.json())
        .then(data => {
            let graphContainer = document.getElementById("graphs-container");

            data.graphs.forEach(filename => {
                let graphCard = document.createElement("div");
                graphCard.className = "graph-card";

                let graphTitle = document.createElement("h2");
                graphTitle.textContent = filename.replace(".html", ""); // ✅ Remove .html from title

                let iframe = document.createElement("iframe");
                iframe.src = "graphs/" + filename;
                iframe.width = "800";
                iframe.height = "600";

                graphCard.appendChild(graphTitle);
                graphCard.appendChild(iframe);
                graphContainer.appendChild(graphCard);
            });
        })
        .catch(error => console.error("Error loading graphs:", error));
});
