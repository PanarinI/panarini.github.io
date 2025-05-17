// assets/js/components.js
document.addEventListener('DOMContentLoaded', function() {
  // Загрузка header
  fetch('components/header.html')
    .then(response => response.text())
    .then(data => {
      document.getElementById('dynamic-header').innerHTML = data;
      setActiveLink();
    });

  // Загрузка footer
  fetch('components/footer.html')
    .then(response => response.text())
    .then(data => {
      document.getElementById('dynamic-footer').innerHTML = data;
    });
});

function setActiveLink() {
  // 1. Получаем текущий путь страницы (например, "/projects/metodica.html")
  const currentPage = location.pathname;

  // 2. Находим ВСЕ ссылки в навигации
  document.querySelectorAll('nav a').forEach(link => {

    // 3. Сравниваем путь ссылки с текущим путём
    if (link.getAttribute('href') === currentPage) {

      // 4. Если совпадает — добавляем класс 'active'
      link.classList.add('active');
    }
  });
}