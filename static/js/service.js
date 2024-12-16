// Главная функция, отвечающая за выбор мастера
document.addEventListener("DOMContentLoaded", () => {
  const masterElements = document.querySelectorAll(".accordion__block[data-master-id]");
  const salonPanel = document.querySelector(".service__salons .panel");
  const servicePanel = document.querySelector(".service__services .panel");

  masterElements.forEach(element => {
    element.addEventListener("click", () => {
      const masterId = element.getAttribute("data-master-id");
      fetchDataAndUpdateUI(masterId, salonPanel, servicePanel);
    });
  });
});

function fetchDataAndUpdateUI(masterId, salonPanel, servicePanel) {
  fetch(`/service?master_id=${masterId}`, {
    headers: { "X-Requested-With": "XMLHttpRequest" },
  })
    .then(response => response.json())
    .then(data => {
      console.log("Полученные данные:", data);

      updateSalonPanel(data.salons, salonPanel);
      updateServicePanel(data.services, servicePanel);

      initializeAccordion();
    })
    .catch(error => {
      console.error("Ошибка при получении данных:", error);
    });
}

function updateSalonPanel(salons, salonPanel) {
  salonPanel.innerHTML = '';
  if (salons && salons.length > 0) {
    salons.forEach(salon => {
      salonPanel.innerHTML += `
        <div class="accordion__block fic">
          <div class="accordion__block_intro">${salon.title}</div>
          <div class="accordion__block_address">${salon.address}</div>
        </div>
      `;
    });
  } else {
    salonPanel.innerHTML = '<div>Нет доступных салонов для этого мастера.</div>';
  }
}

function updateServicePanel(services, servicePanel) {
  servicePanel.innerHTML = '';
  if (services && services.length > 0) {
    const groupedServices = groupServicesByCategory(services);

    for (const [category, services] of Object.entries(groupedServices)) {
      let serviceHTML = `
        <button class="accordion">${category}</button>
        <div class="panel">
          <div class="accordion__block_items">
      `;
      services.forEach(service => {
        serviceHTML += `
          <div class="accordion__block fic">
            <div class="accordion__block_item_intro">${service.name}</div>
            <div class="accordion__block_item_address">${service.price}₽</div>
          </div>
        `;
      });
      serviceHTML += '</div></div>';
      servicePanel.innerHTML += serviceHTML;
    }
  } else {
    servicePanel.innerHTML = '<div>Нет доступных услуг для этого мастера.</div>';
  }
}

function groupServicesByCategory(services) {
  return services.reduce((acc, service) => {
    const categoryName = service.category__name;
    if (!acc[categoryName]) {
      acc[categoryName] = [];
    }
    acc[categoryName].push(service);
    return acc;
  }, {});
}

function initializeAccordion() {
  const accordions = document.querySelectorAll(".accordion");
  accordions.forEach(accordion => {
    accordion.addEventListener("click", () => {
      const panel = accordion.nextElementSibling;
      panel.style.display = panel.style.display === "block" ? "none" : "block";
    });
  });
}
