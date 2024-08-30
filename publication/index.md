---
title: Publications
nav:
  order: 3
---


# **Publication**
<!-- <script src="https://bibbase.org/show?bib=https://hyHarco.github.io/Journal.bib&theme=side&jsonp=1&folding=1&fullnames=1&showSearch=true&commas=true"></script> -->

<!-- ## Publications -->

<div id="publications-list"></div>

<script>
    fetch('publications.json')
        .then(response => response.json())
        .then(data => {
            let publicationsList = document.getElementById('publications-list');
            
            // Sort by year, then by title within the same year
            data.sort((a, b) => b.year - a.year || a.title.localeCompare(b.title));

            let currentYear = null;

            // Process each publication and append to the publications list
            data.forEach(pub => {
                // Check if we need to insert a new year header
                if (pub.year !== currentYear) {
                    currentYear = pub.year;
                    let yearHeader = document.createElement('h3');
                    yearHeader.textContent = currentYear;
                    publicationsList.appendChild(yearHeader);
                }

                let publicationItem = document.createElement('div');
                publicationItem.classList.add('publication-item');
                
                publicationItem.innerHTML = `
                    <div class="publication-details">
                        <strong><a href="${pub.link}" target="_blank">${pub.title}</a></strong><br>
                        ${pub.authors}<br>
                        <em>${pub.journal}</em><br>
                        <span class="publication-category ${pub.category.toLowerCase()}">${pub.category.charAt(0).toUpperCase() + pub.category.slice(1)}</span>
                    </div>
                `;
                
                publicationsList.appendChild(publicationItem);
            });
        })
        .catch(error => console.error('Error fetching publications:', error));
</script>

<style>
    #publications-list h3 {
        margin-top: 1.5em;
        font-size: 1.5em;
        color: #333;
    }
    .publication-item {
        margin-bottom: 1.5em;
    }
    .publication-details {
        text-align: left;
        padding-left: 10px;
    }
    .publication-details a {
        text-decoration: none;
        color: #007BFF;
    }
    .publication-details a:hover {
        text-decoration: underline;
    }
    .publication-details em {
        color: #555;
    }
    .publication-category {
        display: inline-block;
        margin-top: 5px;
        padding: 2px 8px;
        font-size: 0.85em;
        font-weight: bold;
        color: white;
        background-color: #007BFF;
        border-radius: 3px;
        margin-bottom: 5px;
    }
    .publication-category.conference {
        background-color: #28a745; /* Green for conferences */
    }
    .publication-category.journal {
        background-color: #007BFF; /* Blue for journals */
    }
</style>