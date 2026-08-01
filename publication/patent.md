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
            const publicationsList = document.getElementById('publications-list');
            
            // Sort by year descending, then by title within the same year
            data.sort((a, b) => b.year - a.year || a.title.localeCompare(b.title));

            let currentYear = null;

            const statusLabel = {
                'registered': 'Registered',
                'applied': 'Applied',
                'pending': 'Pending'
            };

            const appendBreak = element => element.appendChild(document.createElement('br'));

            data.forEach(pub => {
                if (pub.year !== currentYear) {
                    currentYear = pub.year;
                    const yearHeader = document.createElement('h3');
                    yearHeader.textContent = currentYear ?? 'Pending';
                    publicationsList.appendChild(yearHeader);
                }

                const publicationItem = document.createElement('div');
                publicationItem.classList.add('publication-item');

                const rawStatus = (pub.status || 'pending').toString().toLowerCase();
                const status = statusLabel[rawStatus] ? rawStatus : 'pending';
                const label = statusLabel[status];

                const details = document.createElement('div');
                details.classList.add('publication-details');

                const title = document.createElement('strong');
                title.textContent = pub.title || 'Untitled patent';
                details.appendChild(title);
                appendBreak(details);

                details.appendChild(document.createTextNode(pub.inventors || ''));
                appendBreak(details);

                const applicationNumber = document.createElement('em');
                applicationNumber.textContent = pub.app_no || pub.reg_no || '';
                details.appendChild(applicationNumber);
                appendBreak(details);

                const statusBadge = document.createElement('span');
                statusBadge.classList.add('publication-category', status);
                statusBadge.textContent = label;
                details.appendChild(statusBadge);

                publicationItem.appendChild(details);

                publicationsList.appendChild(publicationItem);
            });
        })
        .catch(error => console.error('Error fetching publications:', error));
</script>
