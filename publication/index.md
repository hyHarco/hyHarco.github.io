---
title: Paper
nav:
  order: 3
---


# **Journal & Conference Papers**

<!-- <script src="https://bibbase.org/show?bib=https://hyHarco.github.io/Journal.bib&theme=side&jsonp=1&folding=1&fullnames=1&showSearch=true&commas=true"></script> -->

<!-- ## Publications -->

<div id="publications-list"></div>

<script>
    fetch('/publication/publications.json')
        .then(response => response.json())
        .then(data => {
            const publicationsList = document.getElementById('publications-list');
            
            // Sort by year, then by title within the same year
            data.sort((a, b) => b.year - a.year || a.title.localeCompare(b.title));

            let currentYear = null;

            const appendBreak = element => element.appendChild(document.createElement('br'));

            // Process each publication and append to the publications list
            data.forEach(pub => {
                // Check if we need to insert a new year header
                if (pub.year !== currentYear) {
                    currentYear = pub.year;
                    const yearHeader = document.createElement('h3');
                    yearHeader.textContent = currentYear;
                    publicationsList.appendChild(yearHeader);
                }

                const publicationItem = document.createElement('div');
                publicationItem.classList.add('publication-item');

                const details = document.createElement('div');
                details.classList.add('publication-details');

                const titleWrapper = document.createElement('strong');
                const titleLink = document.createElement('a');
                titleLink.href = pub.link || '#';
                titleLink.target = '_blank';
                titleLink.rel = 'noopener';
                titleLink.textContent = pub.title || 'Untitled publication';
                titleWrapper.appendChild(titleLink);
                details.appendChild(titleWrapper);
                appendBreak(details);

                details.appendChild(document.createTextNode(pub.authors || ''));
                appendBreak(details);

                const journal = document.createElement('em');
                journal.textContent = pub.journal || '';
                details.appendChild(journal);
                appendBreak(details);

                const category = (pub.category || 'publication').toString();
                const categoryLabel = category.charAt(0).toUpperCase() + category.slice(1);
                const categoryBadge = document.createElement('span');
                categoryBadge.classList.add('publication-category', category.toLowerCase());
                categoryBadge.textContent = categoryLabel;
                details.appendChild(categoryBadge);

                publicationItem.appendChild(details);
                
                publicationsList.appendChild(publicationItem);
            });
        })
        .catch(error => console.error('Error fetching publications:', error));
</script>
