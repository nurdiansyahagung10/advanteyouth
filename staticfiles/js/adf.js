  const navbar = document.querySelector('nav');

 document.querySelector('.second-button').addEventListener('click', function () {
  document.querySelector('.animated-icon2').classList.toggle('open');

});


function removeClassOnSmallScreens() {
  const screenWidth = window.innerWidth;
  const element = document.querySelector('.animated-icon2'); // Ganti dengan selektor elemen Anda

  if (screenWidth >= 991) {
    element.classList.remove('open'); // Ganti dengan nama kelas yang ingin Anda hapus
  }
}

// Panggil fungsi saat halaman dimuat dan saat ukuran layar berubah
window.addEventListener('resize', removeClassOnSmallScreens);


window.addEventListener('scroll', function () {
  if (window.scrollY > 20) {
    navbar.classList.add('scrolled');
    navbar.classList.add('collored');
     document.querySelector('.second-button').addEventListener('click', function () {
      navbar.classList.toggle('scrolled');
});

  } else {
    navbar.classList.remove('scrolled');
    navbar.classList.remove('collored');
  }
});
window.addEventListener('scroll', function () {
  const button = document.querySelector('#scrollToTopBtn');
  if (window.scrollY > 900) {
    button.classList.add('d-lg-block');
  } else {
    button.classList.remove('d-lg-block');
  }
});
