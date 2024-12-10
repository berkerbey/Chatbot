document.addEventListener("DOMContentLoaded", () => {
    const uploadForm = document.getElementById("uploadForm");
    const popup = document.getElementById("popup");
    const fileList = document.getElementById("files");
    const chatSection = document.getElementById("chatSection");
    const questionInput = document.getElementById("question");
    const askButton = document.getElementById("askButton");
    const answerDiv = document.getElementById("answer");

    // Dosya yükleme işlemi
    if (uploadForm) {
        uploadForm.addEventListener("submit", async (event) => {
            event.preventDefault(); // Sayfa yenilenmesini engelle

            const formData = new FormData(uploadForm);

            try {
                const response = await fetch("/upload", {
                    method: "POST",
                    body: formData,
                });

                const result = await response.json();

                // Popup mesajını göster
                popup.textContent = result.message || result.error;
                popup.classList.remove("hidden");
                popup.classList.add(response.ok ? "success" : "error");

                // 5 saniye sonra popup'ı gizle
                setTimeout(() => {
                    popup.classList.add("hidden");
                }, 5000);

                // Dosyalar listesini güncelle
                if (response.ok) loadFiles();
            } catch (error) {
                console.error("Dosya yüklenirken bir hata oluştu:", error);
                popup.textContent = "Bir hata oluştu. Lütfen tekrar deneyin.";
                popup.classList.remove("hidden");
                popup.classList.add("error");
            }
        });
    }

    // Yüklenen dosyaları listeleme
    async function loadFiles() {
        const userId = "1"; // Varsayılan kullanıcı ID'si
        try {
            const response = await fetch(`/files/${userId}`);
            if (!response.ok) {
                throw new Error("Dosyalar yüklenirken hata oluştu.");
            }
            const files = await response.json();

            // Dosya listesini temizle ve yeniden oluştur
            fileList.innerHTML = "";
            files.forEach(file => {
                const li = document.createElement("li");
                li.textContent = file.name;
                li.dataset.fileId = file.id;
                li.classList.add("file-item");
                li.addEventListener("click", () => selectFile(file.id));
                fileList.appendChild(li);
            });
        } catch (error) {
            console.error(error);
            fileList.innerHTML = `<p style="color:red;">Dosyalar yüklenemedi.</p>`;
        }
    }

    // Dosya seçimi işlemi
    function selectFile(fileId) {
        const userId = "1"; // Varsayılan kullanıcı ID'si
        const chatSection = document.getElementById("chatSection");
        const answerDiv = document.getElementById("answer");

        // Seçilen dosyayı işleme isteği gönder
        fetch(`/process/${userId}/${fileId}`, {
            method: "POST",
        })
            .then(response => response.json())
            .then(result => {
                if (result.message) {
                    console.log(result.message);
                    chatSection.style.display = "block";
                    chatSection.dataset.selectedFileId = fileId; // Seçilen dosyayı sakla
                    answerDiv.textContent = ""; // Önceki yanıtları temizle
                } else {
                    console.error(result.error);
                    alert(result.error || "Dosya işlenemedi.");
                }
            })
            .catch(error => {
                console.error("Dosya işlenirken hata oluştu:", error);
                alert("Dosya işlenirken bir hata oluştu. Lütfen tekrar deneyin.");
            });
    }

    // Soru sorma işlemi
    if (askButton) {
        askButton.addEventListener("click", async () => {
            const fileId = chatSection.dataset.selectedFileId;
            const userId = "1"; // Varsayılan kullanıcı ID'si
            const question = questionInput.value.trim();

            if (!fileId) {
                answerDiv.textContent = "Lütfen bir dosya seçin.";
                return;
            }

            if (!question) {
                answerDiv.textContent = "Lütfen bir soru yazın.";
                return;
            }

            try {
                // Soru gönder ve yanıt al
                const response = await fetch(`/query/${userId}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ question })
                });

                const result = await response.json();
                if (response.ok) {
                    answerDiv.textContent = result.answer || "Yanıt alınamadı.";
                } else {
                    answerDiv.textContent = result.error || "Bir hata oluştu.";
                }
            } catch (error) {
                console.error(error);
                answerDiv.textContent = "Bir hata oluştu. Lütfen tekrar deneyin.";
            }
        });
    }

    // Sayfa yüklendiğinde dosyaları yükle
    loadFiles();
});
