document.addEventListener('DOMContentLoaded', function() {
  // Аварийный заголовок (на случай ошибки)
  const fallbackHeader = `
    <nav class="navbar" style="background: #ffcccc; padding: 10px;">
      <a href="/" class="logo">
        <span class="logo-title">Основная навигация (ошибка загрузки)</span>
      </a>
      <ul class="nav-links">
        <li><a href="/projects/about_me.html">Об авторе</a></li>
        <li><a href="#contacts">Контакты</a></li>
      </ul>
    </nav>
  `;

  // Загрузка header с обработкой ошибок
  loadComponent({
    url: '/components/header.html',
    targetId: 'dynamic-header',
    fallback: fallbackHeader,
    onSuccess: () => {
      // Кастомный заголовок из data-атрибута
      const customLogoTitle = document.body.dataset.logoTitle;
      if (customLogoTitle) {
        const titleSpan = document.querySelector('.logo-title');
        if (titleSpan) titleSpan.textContent = customLogoTitle;
      }
      
      // Подсветка активной ссылки
      setActiveLink();
    }
  });

  // Загрузка footer
  loadComponent({
    url: '/components/footer.html',
    targetId: 'dynamic-footer',
    fallback: '<footer style="padding: 20px; background: #eee;">Футер не загрузился</footer>'
  });
});

/**
 * Универсальная функция загрузки компонентов
 */
function loadComponent({ url, targetId, fallback = '', onSuccess = () => {} }) {
  const target = document.getElementById(targetId);
  if (!target) {
    console.error(`Элемент #${targetId} не найден`);
    return;
  }

  fetch(url)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.text();
    })
    .then(data => {
      target.innerHTML = data;
      onSuccess();
    })
    .catch(error => {
      console.error(`Ошибка загрузки ${url}:`, error);
      target.innerHTML = fallback;
    });
}

/**
 * Подсветка активной ссылки в навигации
 */
function setActiveLink() {
  const currentPage = location.pathname;
  
  document.querySelectorAll('nav a').forEach(link => {
    const linkPath = link.getAttribute('href');

    // Сравниваем пути, игнорируя параметры запроса
    if (linkPath && currentPage.startsWith(linkPath.split('?')[0])) {
      link.classList.add('active');
    }
  });
}