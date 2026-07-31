---
title: Patent
nav:
  order: 3
---


# **Patents**

<div id="publications-list"></div>

<script>
    fetch('/publication/patents.json')
        .then(response => response.json())
        .then(data => {
            let publicationsList = document.getElementById('publications-list');
            
            // Sort by year descending, then by title within the same year
            data.sort((a, b) => b.year - a.year || a.title.localeCompare(b.title));

            let currentYear = null;

            const statusLabel = {
                'registered': 'Registered',
                'applied': 'Applied',
                'pending': 'Pending'
            };

            data.forEach(pub => {
                if (pub.year !== currentYear) {
                    currentYear = pub.year;
                    let yearHeader = document.createElement('h3');
                    yearHeader.textContent = currentYear ?? 'Pending';
                    publicationsList.appendChild(yearHeader);
                }

                let publicationItem = document.createElement('div');
                publicationItem.classList.add('publication-item');

                const label = statusLabel[pub.status] ?? pub.status;

                publicationItem.innerHTML = `
                    <div class="publication-details">
                        <strong>${pub.title}</strong><br>
                        ${pub.inventors}<br>
                        <em>${pub.app_no || pub.reg_no || ''}</em><br>
                        <span class="publication-category ${pub.status}">${label}</span>
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
        border-radius: 3px;
        margin-bottom: 5px;
    }
    .publication-category.registered {
        background-color: #007BFF; /* Blue - Registered */
    }
    .publication-category.applied {
        background-color: #28a745; /* Green - Applied */
    }
    .publication-category.pending {
        background-color: #6c757d; /* Gray - Pending */
    }
</style>