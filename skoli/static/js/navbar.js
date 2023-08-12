let hamburgurBtn = document.getElementById("navbar-hamburger-btn");

hamburgurBtn.addEventListener('click', showOrHideNavContent);

function showOrHideNavContent() {
    let navContent = document.getElementById("navigation");
    let contentDisplayed

    if (navContent.className == 'collapse navbar-collapse pt-3 pb-2 py-lg-0 w-100') {
        navContent.className = "collapse navbar-collapse pt-3 pb-2 py-lg-0 w-100 show"
    }
    else if (navContent.className == 'collapse navbar-collapse pt-3 pb-2 py-lg-0 w-100 show') {
        navContent.className = "collapse navbar-collapse pt-3 pb-2 py-lg-0 w-100"
    }

}