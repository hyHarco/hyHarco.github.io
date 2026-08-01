// Mobile navigation menu and dropdown controls.
document.addEventListener("DOMContentLoaded", function () {
  const header = document.querySelector("header[data-mobile-menu]");
  if (!header) return;

  const menuButton = header.querySelector(".mobile_menu_toggle");
  const navigation = header.querySelector("#site-navigation");
  const mobileQuery = window.matchMedia("(max-width: 600px)");

  function setSubnavOpen(container, open) {
    const button = container.querySelector(".subnavbtn, .subnavbtn-research");

    container.setAttribute("data-subnav-open", open ? "true" : "false");
    if (button) button.setAttribute("aria-expanded", open ? "true" : "false");
  }

  function closeSubnavs(except) {
    header.querySelectorAll(".subnav, .subnav-research").forEach(function (container) {
      if (container !== except) setSubnavOpen(container, false);
    });
  }

  function setMobileMenuOpen(open) {
    header.setAttribute("data-mobile-menu-open", open ? "true" : "false");
    if (menuButton) {
      menuButton.setAttribute("aria-expanded", open ? "true" : "false");
      menuButton.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
    }
    if (!open) closeSubnavs();
  }

  if (menuButton && navigation) {
    menuButton.addEventListener("click", function () {
      setMobileMenuOpen(header.getAttribute("data-mobile-menu-open") !== "true");
    });

    navigation.addEventListener("click", function (event) {
      const link = event.target instanceof Element ? event.target.closest("a") : null;
      if (link && mobileQuery.matches) setMobileMenuOpen(false);
    });
  }

  header.querySelectorAll(".subnav, .subnav-research").forEach(function (container) {
    const button = container.querySelector(".subnavbtn, .subnavbtn-research");
    if (!button) return;

    button.addEventListener("click", function () {
      const target = button.getAttribute("data-nav-target");

      if (!mobileQuery.matches) {
        if (target) window.location.href = target;
        return;
      }

      const nextOpen = container.getAttribute("data-subnav-open") !== "true";
      closeSubnavs(container);
      setSubnavOpen(container, nextOpen);
    });
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") setMobileMenuOpen(false);
  });

  function handleViewportChange() {
    if (!mobileQuery.matches) {
      setMobileMenuOpen(false);
      closeSubnavs();
    }
  }

  if (mobileQuery.addEventListener) {
    mobileQuery.addEventListener("change", handleViewportChange);
  } else {
    mobileQuery.addListener(handleViewportChange);
  }
});
