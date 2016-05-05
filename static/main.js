
function get_titles_ids() {
    var titles_ids = [];
    $(".title").each(function() {
        titles_ids.push($(this).attr("id"));
    })
    return titles_ids;
}

function callback(item) {
    return function(data) {
        console.log(data);
        $('#header').hide();
        response = JSON.parse(data);
        if (response.status == "SUCCESS") {
            console.log(response.poem);
//                console.log($(item));
            $(item).show();
            $('<p/>', {html: response.poem, "class": 'poem'}).appendTo(item);
        }
        else {
            console.log(response.message);
            item.hide();
        }
    };
}

$(document).ready(function() {
    var img = new Image();
        img.onload = function() {
            $("body").addClass("bg");
            //the callback function call here
            $(".title").each(function() {
                $.get("/poem/".concat($(this).attr("id")), callback($(this)));
            })
        };
        img.src = 'static/texture1.jpg';
})