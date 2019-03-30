
function image_viewer(post_id) {
    new Viewer(document.getElementById('images_' + post_id));
}

function unlike(post, reblog) {
    data = {
        "id": post,
        "reblog_key": reblog
    };
    $.post({
        type: 'POST',
        url: '/api/unlike',
        data: JSON.stringify(data),
        success: function (resp) {
            alert('data: ' + resp);
        },
        contentType: "application/json",
        dataType: 'json'
    });
}

function like(post, reblog) {

    data = {
        "id": post,
        "reblog_key": reblog
    };
    $.post({
        type: 'POST',
        url: '/api/relike',
        data: JSON.stringify(data),
        success: function (resp) {
            alert('data: ' + resp);
            console.log(resp)
        },
        contentType: "application/json",
        dataType: 'json'
    });
}

likes.forEach(function (s) {
    image_viewer(s[0]);
});

