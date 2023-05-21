var markSuccess = function (response, notification) {
    if (response.action == 'read') {
        var mkClass = readNotificationClass;
        var rmClass = unreadNotificationClass;
        var action = 'unread';
    } else {
        mkClass = unreadNotificationClass;
        rmClass = readNotificationClass;
        action = 'read';
    }
    notification.closest(nfSelector).removeClass(rmClass).addClass(mkClass);
    notification.attr('data-mark-action', action);

    toggle_text = notification.attr('data-toggle-text') || 'Mark as ' + action;
    notification.attr('data-toggle-text', notification.html());
    notification.html(toggle_text);

    notification_li = notification.parent().parent()
    if (notification_li.hasClass('alert-light') == true){
        notification_li.removeClass('alert-light').addClass('alert-info');
    }else{
        notification_li.removeClass('alert-info').addClass('alert-light');
    }
};