document.addEventListener('DOMContentLoaded', function () {
    // 원격 .bib 파일을 불러옵니다.
    fetch('https://hyHarco.github.io/Journal.bib')
      .then(response => response.text())
      .then(data => {
        const bibtex = new BibTeX();
        bibtex.content = data;
        bibtex.parse();
        
        const entries = bibtex.getEntries();
        
        // 논문 목록을 표시할 요소를 가져옵니다.
        const publicationsContainer = document.querySelector('#publications');
        
        for (const entry of entries) {
          // 각 논문의 제목, 저자, 출판 정보 등을 가져옵니다.
          const title = entry.getField('title');
          const authors = entry.getField('author');
          const year = entry.getField('year');
          const venue = entry.getField('journal') || entry.getField('booktitle');
          
          // 각 논문 정보를 HTML로 변환합니다.
          const publicationHTML = `
            <div class="publication">
              <h3 class="publication-title">${title}</h3>
              <p class="publication-authors">${authors}</p>
              <p class="publication-venue">${venue}, ${year}</p>
            </div>
          `;
          
          // 논문 목록에 새로운 논문 정보를 추가합니다.
          publicationsContainer.innerHTML += publicationHTML;
        }
      });
  });
  