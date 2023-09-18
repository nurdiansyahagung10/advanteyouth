
 document.querySelector('.kategori').addEventListener('click', function () {
  document.querySelector('.animated-ic  on2').classList.toggle('open');
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
  const navbar = document.querySelector('nav');
  if (window.scrollY > 20) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
});

var element = document.querySelector('.nav-nama');
var maxLength = 10; // Ubah sesuai kebutuhan Anda

if (element.textContent.length > maxLength) {
  element.textContent = element.textContent.substring(0, maxLength) + '...';
}