function validate(file) {
    var ext = file.split(".");
    ext = ext[ext.length-1].toLowerCase();
    var arrayExtensions = ["json"];

    if (arrayExtensions.lastIndexOf(ext) === -1) {
        alert("Wrong extension type.");
        $("#jsonFile").val("");
    }
}
$(document).ready(function (e) {
    $('#upload').on('click', function () {
        var form_data = new FormData();
        var ins = document.getElementById('jsonFile').files.length;

        if (ins === 0 ) {
            $('#msg').html('<span style="color:red">Select at least valid json file</span>');
            return;
        }

        form_data.append("file", document.getElementById('jsonFile').files[0]);

        $.ajax({
            url: '/api/upload', // point to server-side URL
            dataType: 'json', // what to expect back from server
            cache: false,
            contentType: false,
            processData: false,
            data: form_data,
            type: 'post',
            success: function (response) { // display success response
                $('#msg').html('');
                $.each(response, function (key, data) {
                    if (key !== 'message') {
                        $('#msg').append(key + ' -> ' + data + '<br/>');
                    } else {
                        $('#msg').append(data + '<br/>');
                    }
                })
            },
            error: function (response) {
                $('#msg').html(response.message); // display error response
            }
        });
    });
});