window.onload = () => {
  const dropDownBtn = document.getElementById('dropdown-toggle');
  const dropDownMenu = document.getElementById('dropdown-menu');
  let dropdownOpen = false;

  const closeDropdown = () => {
    dropDownMenu.classList.remove('show');
    dropDownMenu.classList.add('hide-menu');
    dropDownBtn.setAttribute('aria-expanded', 'false');
    dropdownOpen = false;
  };

  const openDropdown = () => {
    dropDownMenu.classList.remove('hide-menu');
    dropDownMenu.classList.add('show');
    dropDownBtn.setAttribute('aria-expanded', 'true');
    dropdownOpen = true;
  };

  document.addEventListener('click', (event) => {
    if (!dropDownMenu.contains(event.target) && !dropDownBtn.contains(event.target)) {
      closeDropdown();
    }
  });

  dropDownBtn.addEventListener('click', () => {
    dropdownOpen ? closeDropdown() : openDropdown();
  });
};






