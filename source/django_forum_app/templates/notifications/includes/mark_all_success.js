var markAllSuccess = function (response) {
    //console.log(response);
    // console.log(response.action);
    notification_li_s = $('.notification-box-list li');
    notification_li_btns = $('.notification-box-list li .mark-notification');
    if (response.action == 'read') {
        var mkClass = readNotificationClass;
        var rmClass = unreadNotificationClass;
        notification_li_s.removeClass('alert-info').addClass('alert-light');
        notification_li_btns.html('Mark as unread');
    } else {
        mkClass = unreadNotificationClass;
        rmClass = readNotificationClass;
        notification_li_s.removeClass('alert-light').addClass('alert-info');
        notification_li_btns.html('Mark as read');
    }
    // console.log(mkClass);
    // console.log(rmClass);
    $(nfSelector).removeClass(rmClass).addClass(mkClass);
};