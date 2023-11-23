$(document).ready(function() {
    $('#upload-form').on('submit', function(e) {
        e.preventDefault();
        var formData = new FormData(this);
        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(data) {
                window.location.href = data;
            },
            error: function(xhr, status, error) {
                console.error("Upload failed:", error);
            }
        });
    });
});