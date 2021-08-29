$(".card-id").hover(function() {
    $(this).addClass("blur");
}, function(){
    $(this).removeClass("blur");
});

$(document).on('click', '.add-item-button', function (e) {
    e.preventDefault();
    // console.log($(this).val());
    // console.log($(this).data('url'));
    $.ajax({
        type: 'POST',
        url: $(this).data('url'),
        data: {
            productId: $(this).val(),
            productQuantity: 1,
            csrfmiddlewaretoken: $('#csrfmiddlewaretoken').val(),
            action: 'post'
        },
        success: function (json) {

        },
        error: function (xhr, errmsg, err) {}
    });
});

$(document).on("click", ".remove-item-button", function (e) {
    e.preventDefault();
    let removedProductId = $(this).data('index')
    $.ajax({
        type: 'POST',
        url: $(this).data('url'),
        data: {
            productId: removedProductId,
            csrfmiddlewaretoken: $('#csrfmiddlewaretoken').val(),
            action: 'delete'
        },
        success: function (json) {
            $(".table-item[data-index='"+ removedProductId +"']").remove();
            setTimeout(function () {
                location.reload();
            }, 200);
        },
        error: function (xhr, errmsg, err) {
            console.log(errmsg)
        }
    });
})
