var deleteSuccess = function (response, notification) {
    notification_li = notification.parent().parent()
    notification_li.fadeOut(300, function(){
        notification_li.remove();
    })
};