$(document).ready(function() {

    $(".download-button").click(function() {
        var $genreInput = $.trim($("#genre").val());
        var $keyInput = $.trim($("#key").val());
        var $bpmInput = $.trim($("#bpm").val());

        if ($genreInput == '' || $keyInput == '' || $bpmInput == '') {
            alert("Please fill in all of the required input values");
        } else {
            $("#main").fadeOut('slow', function() {
                $("#downloading").show();
            });
            $.post("http://localhost:5000/download", {
                genre: $genreInput,
                key: $keyInput,
                bpm: $bpmInput
            }, function(response, status) {
                alert(response.message);
                location.reload(true);
            });
        }
    });

    $(".play-button").click(function() {
        var $row = $(this).closest("tr");
        var $text = $row.find(".track-name").text();

        $.post("http://localhost:5000/play", {
            name: $text
        }, function(response, status) {
            alert(response.message);
        });
    });

    $(".delete-button").click(function() {
        var $row = $(this).closest("tr");
        var $text = $row.find(".track-name").text();

        $.post("http://localhost:5000/delete", {
            name: $text
        }, function(response, status) {
            alert(response.message);
            location.reload(true);
        });
    });

});
