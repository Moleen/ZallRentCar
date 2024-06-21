document.addEventListener('DOMContentLoaded', function () {
    // Event listener untuk membuka modal edit
    document.getElementById('editIcon').addEventListener('click', function () {
        $('#editModal').modal('show');
    });

    // Event listener untuk tombol Cancel
    document.getElementById('cancelChanges').addEventListener('click', function () {
        // Menutup modal
        $('#editModal').modal('hide');
    });

    document.getElementById('saveChanges').addEventListener('click', function () {
        // Mengumpulkan data dari form
        var formData = new FormData();
        formData.append('username', document.getElementById('editName').value);
        formData.append('email', document.getElementById('editEmail').value);
        formData.append('phone', document.getElementById('editPhone').value);
        formData.append('address', document.getElementById('editAddress').value);

        // Jika ada file gambar yang diupload, tambahkan ke formData
        if (document.getElementById('editProfileImage').files[0]) {
            formData.append('profile_image', document.getElementById('editProfileImage').files[0]);
        }

        // Tampilkan animasi loading
        document.getElementById('loadingSpinner').style.display = 'flex';

        // Mengirimkan permintaan ke server
        fetch('/profile', {
            method: 'POST',
            body: formData,
            headers: {
                'Authorization': `Bearer ${document.cookie.split('=')[1]}`
            }
        })
            .then(response => {
                // Memeriksa apakah respons dari server sukses
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Menangani respons dari server
                if (data.result === 'success') {
                    // Memperbarui UI dengan data baru
                    document.getElementById('email').innerText = document.getElementById('editEmail').value;
                    document.getElementById('phone').innerText = document.getElementById('editPhone').value;
                    document.getElementById('address').innerText = document.getElementById('editAddress').value;

                    // Memperbarui gambar profil jika ada gambar baru yang diupload
                    if (document.getElementById('editProfileImage').files[0]) {
                        var reader = new FileReader();
                        reader.onload = function (e) {
                            document.getElementById('profileImage').src = e.target.result;
                        }
                        reader.readAsDataURL(document.getElementById('editProfileImage').files[0]);
                    }

                    // Menutup modal dan menampilkan pesan sukses
                    $('#editModal').modal('hide');
                    alert('Profil berhasil diperbarui!');

                    // Mereload halaman setelah profil berhasil diperbarui
                    window.location.reload();
                } else {
                    // Menampilkan pesan kesalahan dari server
                    alert(data.msg);
                }
            })
            .catch(error => {
                // Menangani kesalahan yang terjadi saat pembaruan profil
                console.error('Error:', error);
                alert('Terjadi kesalahan saat memperbarui profil. Silakan coba lagi nanti.');
            })
            .finally(() => {
                // Sembunyikan animasi loading
                document.getElementById('loadingSpinner').style.display = 'none';
            });
    });
});
